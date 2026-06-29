# 기업 추천을 위한 Sentence-BERT 임베딩
# pip install sentence-transformers (내부적으로 PyTorch 사용)

from sentence_transformers import SentenceTransformer
import torch
import numpy as np

class EmbeddingModel:
    def __init__(self):
        # 한국어 지원 모델 선택
        self.model = SentenceTransformer("snunlp/KR-SBERT-V40K-klueNLI-augSTS")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = self.model.to(self.device)

    def encode(self, texts: list[str]) -> np.ndarray:
        with torch.no_grad():
            embeddings = self.model.encode(
                texts,
                convert_to_tensor=True,
                device=self.device,
                batch_size=32
            )
        return embeddings.cpu().numpy()

    def similarity(self, query_vec: np.ndarray, corpus_vecs: np.ndarray) -> np.ndarray:
        # 코사인 유사도
        q = query_vec / np.linalg.norm(query_vec)
        c = corpus_vecs / np.linalg.norm(corpus_vecs, axis=1, keepdims=True)
        return c @ q  # shape: (N,)