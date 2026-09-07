import json
from src.tools.registry import register_tool
from src.schemas.tools import SearchInformationArgs, RetrieveDocumentArgs

_LOCAL_CORPUS = {
    "doc-01": {
        "title": "AI Customer Support Market Overview 2026",
        "text": "The global AI-powered customer support market is valued at $2.4bn in 2026. Key players include Vendor A, Vendor B, and Vendor C."
    },
    "doc-02": {
        "title": "Vendor B Enterprise Pricing & Features",
        "text": "Vendor B provides advanced omnichannel routing. Enterprise tier pricing is customized upon request."
    }
}

@register_tool(
    name="search_information",
    description="Searches approved sources and corpus for market data, vendor info, and pricing.",
    args_schema=SearchInformationArgs,
    permission_level="read"
)
def search_information(query: str, source_type: str = "corpus", max_results: int = 5, recency_window: str = "any") -> list:
    results = []
    q_lower = query.lower()
    for doc_id, doc in _LOCAL_CORPUS.items():
        if q_lower in doc["title"].lower() or q_lower in doc["text"].lower():
            results.append({
                "id": doc_id,
                "title": doc["title"],
                "source_identifier": f"corpus://{doc_id}",
                "snippet": doc["text"][:150] + "..."
            })
    return results[:max_results]

@register_tool(
    name="retrieve_document",
    description="Retrieves full text and metadata for a specific document ID.",
    args_schema=RetrieveDocumentArgs,
    permission_level="read"
)
def retrieve_document(document_id: str, section: str = None) -> dict:
    if document_id not in _LOCAL_CORPUS:
        raise ValueError(f"Document ID '{document_id}' does not exist in the index.")
    doc = _LOCAL_CORPUS[document_id]
    return {
        "document_id": document_id,
        "title": doc["title"],
        "full_text": doc["text"],
        "provenance": "Local Verified Corpus"
    }