SITES = [

    # 🎓 Academic & Preprint Servers
    "https://arxiv.org",                          # Top academic preprints (AI, ML, CV, NLP)
    "https://paperswithcode.com",                 # Papers + code for ML/AI
    "https://openaccess.thecvf.com",              # CVPR/ICCV/ECCV open access papers
    "https://www.semanticscholar.org",            # AI/ML focused paper search
    "https://pubmed.ncbi.nlm.nih.gov",            # AI in healthcare & medicine
    "https://aclanthology.org",                   # NLP conference papers

    # 🧠 Research Labs & Organizations
    "https://openai.com/blog",                    # OpenAI research articles
    "https://deepmind.com/blog",                  # DeepMind’s research blog
    "https://ai.googleblog.com",                  # Google Research blog (AI/ML)
    "https://huggingface.co/blog",                # Transformers, tools, demos
    "https://ai.meta.com/blog",                   # Meta AI research blog
    "https://allenai.org/news",                   # Allen Institute for AI
    "https://microsoft.com/en-us/research",       # Microsoft Research site
    "https://research.ibm.com/blog",              # IBM AI blog
    "https://www.nvidia.com/en-us/research",      # NVIDIA AI research
    ]


from utils import summarize, generate_report
from web_scraper import scrape_websites

def run_agentic_research(query):
    try:
        # ✅ Now passing both required arguments
        pages = scrape_websites(query, SITES)

        if not pages or all(len(p.get("text", "")) < 50 for p in pages):
            print("⚠️ No relevant pages found. Falling back to Groq model.")
            summary = summarize([{"text": ""}], query)
            return {
                "summary": summary,
                "sources": [],
                "pages": [],
                "fallback": True
            }

        summary = summarize(pages, query)
        # sources = [p.get("site","") for p in pages]
        sources = [p.get("url") or p.get("site", "") for p in pages]
        return {
            "summary": summary,
            "sources": sources,
            "pages": pages,
            "fallback": False
        }

    except Exception as e:
        print("❌ Error in run_agentic_research:", e)
        return {
            "summary": f"❌ Research failed. Error: {str(e)}",
            "sources": [],
            "pages": [],
            "fallback": True
        }

