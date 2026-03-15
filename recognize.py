import cv2
import insightface
import pickle
import numpy as np
import os

# ---------------- Load Model ----------------
app = insightface.app.FaceAnalysis(name="buffalo_l")
app.prepare(ctx_id=0)

# ---------------- Load Embeddings ----------------
with open("embeddings/student_embeddings.pkl", "rb") as f:
    known_embeddings = pickle.load(f)

# ---------------- Cosine Similarity ----------------
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def recognize_faces(image_path):

    img = cv2.imread(image_path)

    faces = app.get(img)

    total_faces = len(faces)

    recognized_names = []
    unknown_count = 0

    for face in faces:

        embedding = face.embedding
        bbox = face.bbox.astype(int)

        best_match = "Unknown"
        best_score = 0

        # compare with stored embeddings
        for name, db_embeddings in known_embeddings.items():

            for db_embedding in db_embeddings:

                score = cosine_similarity(embedding, db_embedding)

                if score > best_score:
                    best_score = score
                    best_match = name

        if best_score > 0.5:
            label = best_match
            recognized_names.append(best_match)
            color = (0,255,0)  # green
        else:
            label = "Unknown"
            unknown_count += 1
            color = (0,0,255)  # red

        x1,y1,x2,y2 = bbox

        # draw rectangle
        cv2.rectangle(img,(x1,y1),(x2,y2),color,2)

        # draw name
        cv2.putText(img,label,(x1,y1-10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,color,2)

    os.makedirs("results", exist_ok=True)

    output_path = "results/result.jpg"

    cv2.imwrite(output_path,img)

    return {
        "total_faces": total_faces,
        "recognized": list(set(recognized_names)),
        "recognized_count": len(recognized_names),
        "unknown_count": unknown_count,
        "output_image": output_path
    }