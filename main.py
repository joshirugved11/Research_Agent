import os
import traceback
from logic.core import fetch_papers, summarize_text
from models.utils import read_text_from_file, save_summary_to_pdf

def save_paper_text(paper, index):
    """Save the paper content to data/papers/ and return the saved file path."""
    os.makedirs("data/papers", exist_ok=True)
    safe_title = paper['title'].replace(" ", "_").replace("/", "_")[:50]
    file_path = os.path.join("data/papers", f"{index+1}_{safe_title}.txt")
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(paper['content'])
    
    return file_path

def get_paper_display(paper):
    """Formats the paper details for display."""
    display = f"{paper['title']}"
    if paper.get('authors'):
        display += f" by {', '.join(paper['authors'])}"
    if paper.get('year'):
        display += f" ({paper['year']})"
    return display

def select_source():
    print("\n📚 Choose a source:")
    print("1. Semantic Scholar")
    print("2. PubMed")
    print("3. Arxiv")
    print("4. CORE")

    source_map = {
        "1": "Semantic Scholar",
        "2": "PubMed",
        "3": "Arxiv",
        "4": "CORE"
    }

    choice = input("Enter choice (1/2/3/4): ").strip()
    return source_map.get(choice)

def main():
    source = select_source()
    if not source:
        print("❌ Invalid choice.")
        return

    query = input("\n🔍 Enter your search query: ")

    try:
        papers = fetch_papers(source, query)
    except Exception as e:
        print(f"❌ Error fetching papers: {e}")
        print(traceback.format_exc())
        return

    if not papers:
        print("❌ No papers found.")
        return
    
    # save fetched paper contents
    print("\n📥 Saving fetched papers...")
    saved_papers = []
    for i, paper in enumerate(papers):
        path = save_paper_text(paper, i)
        paper['file_path'] = path
        saved_papers.append(paper)

    # Display list
    print("\n📄 Available Papers:")
    for i, paper in enumerate(saved_papers):
        print(f"{i+1}. {get_paper_display(paper)}")

    try:
        selected_index = int(input("\nSelect paper to summarize (1-N): ")) - 1
        selected_paper = saved_papers[selected_index]
    except (IndexError, ValueError):
        print("❌ Invalid selection.")
        return
    
    print(f"\n⏳ Summarizing: {selected_paper['title']}")

    text = read_text_from_file(selected_paper['file_path'])
    summary = summarize_text(text)

    print("\n✅ Summary generated!\n")

    # Save outputs
    filename = selected_paper['title']
    os.makedirs("data/summaries", exist_ok=True)
    save_summary_to_pdf(summary, filename=filename)

    # also save summary as a txt file
    safe_title = filename.replace(" ", "_").replace("/", "_")[:50]
    txt_path = os.path.join("data/summaries", f"{safe_title}.txt")
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(summary)

    print(f"✅ Summary saved to PDF and TXT in 'data/summaries/'")

if __name__ == "__main__":
    main()