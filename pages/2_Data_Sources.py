import streamlit as st
import pandas as pd
import plotly.express as px
from neo4j import GraphDatabase, exceptions

# --- Neo4j Connection and Data Fetching ---

@st.cache_resource
def get_neo4j_driver():
    """
    Establishes a connection to the Neo4j database using credentials
    from Streamlit's secrets management.
    The _resource annotation ensures the connection is cached and reused.
    """
    try:
        uri = st.secrets["neo4j"]["uri"]
        user = st.secrets["neo4j"]["user"]
        password = st.secrets["neo4j"]["password"]
        database = st.secrets["neo4j"]["database"]
        return GraphDatabase.driver(uri, auth=(user, password), database=database)
    except KeyError:
        st.error("Neo4j credentials not found in secrets.toml. Please add them.")
        return None
    except exceptions.AuthError:
        st.error("Neo4j authentication failed. Please check your credentials in secrets.toml.")
        return None
    except Exception as e:
        st.error(f"Failed to connect to Neo4j: {e}")
        return None

@st.cache_data(ttl=60) # Cache data for 60 seconds
def fetch_graph_stats(_driver):
    """
    Queries the Neo4j database to get live statistics on nodes and relationships.
    The _data annotation caches the result of the query.
    """
    if not _driver:
        return None
    
    try:
        with _driver.session() as session:
            # Query for node counts by label
            node_counts = session.run("""
                MATCH (n)
                RETURN labels(n)[0] AS label, count(n) AS count
            """).data()
            
            # Query for relationship counts by type
            rel_counts = session.run("""
                MATCH ()-[r]->()
                RETURN type(r) AS type, count(r) AS count
            """).data()

        # Process the results into a more usable dictionary
        stats = {
            "node_types": {item['label']: item['count'] for item in node_counts if item['label']},
            "relationship_types": {item['type']: item['count'] for item in rel_counts if item['type']},
        }
        stats["total_nodes"] = sum(stats["node_types"].values())
        stats["total_relationships"] = sum(stats["relationship_types"].values())
        return stats
    except exceptions.ServiceUnavailable:
        st.warning("Could not connect to the Neo4j database. Displaying mock data. Please ensure the database is running.")
        return None
    except Exception as e:
        st.error(f"An error occurred while querying the database: {e}")
        return None

# --- UI Rendering ---

def main():
    """Main function to render the Data Sources page."""
    st.set_page_config(
        page_title="Data Sources - ASU Chatbot",
        page_icon="📊",
        layout="wide"
    )

    # Custom CSS (unchanged)
    st.markdown("""
    <style>
        .data-header { font-size: 2.5rem; font-weight: bold; color: #0033A0; text-align: center; margin-bottom: 2rem; }
        .source-card { background-color: #f8f9fa; padding: 1.5rem; border-radius: 10px; border-left: 5px solid #FFC72C; margin: 1rem 0; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
        .stats-card { background-color: #0033A0; color: white; padding: 1.5rem; border-radius: 10px; text-align: center; }
        .metric-value { font-size: 2rem; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<h1 class="data-header">📊 Live Data Source & Knowledge Graph</h1>', unsafe_allow_html=True)
    
    st.markdown("This page provides a live dashboard of the chatbot's knowledge graph, with statistics queried directly from the Neo4j database.")
    
    # --- Fetch Live Data ---
    driver = get_neo4j_driver()
    graph_stats = fetch_graph_stats(driver)

    if not graph_stats:
        # If connection fails, we stop here as there's no data to display
        st.stop()

    # --- Display Live Statistics ---
    st.header("📈 Live Knowledge Graph Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="stats-card"><h3>Total Nodes</h3><div class="metric-value">{graph_stats.get("total_nodes", 0):,}</div><p>Knowledge entities</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="stats-card"><h3>Total Relationships</h3><div class="metric-value">{graph_stats.get("total_relationships", 0):,}</div><p>Connections</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="stats-card"><h3>Node Types</h3><div class="metric-value">{len(graph_stats.get("node_types", {}))}</div><p>Entity categories</p></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="stats-card"><h3>Relationship Types</h3><div class="metric-value">{len(graph_stats.get("relationship_types", {}))}</div><p>Connection types</p></div>', unsafe_allow_html=True)

    # --- Live Visualizations ---
    st.header("📊 Live Schema Visualizations")
    col1, col2 = st.columns(2)
    with col1:
        node_df = pd.DataFrame(list(graph_stats.get("node_types", {}).items()), columns=['Node Type', 'Count']).sort_values("Count", ascending=False)
        fig_nodes = px.bar(node_df, x='Node Type', y='Count', title="Distribution of Node Types", color_discrete_sequence=['#0033A0'])
        st.plotly_chart(fig_nodes, use_container_width=True)
    
    with col2:
        rel_df = pd.DataFrame(list(graph_stats.get("relationship_types", {}).items()), columns=['Relationship Type', 'Count']).sort_values("Count", ascending=False)
        fig_rels = px.bar(rel_df, x='Relationship Type', y='Count', title="Distribution of Relationship Types", color_discrete_sequence=['#FFC72C'])
        st.plotly_chart(fig_rels, use_container_width=True)
    
    # The rest of the page (Data Source Card and Pipeline Info) remains relevant and unchanged
    st.header("🔗 Primary Data Source")
    st.markdown("""
    <div class="source-card">
        <h3>📚 Undergraduate Catalog PDF</h3>
        <p><strong>Content:</strong> The chatbot's knowledge is exclusively derived from the official <strong>undergraduate-catalog.pdf</strong>.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.header("⚙️ Data Ingestion Pipeline")
    pipeline_steps = [
        "**1. Structured Data Extraction:** An LLM extracts a JSON hierarchy of the university structure from the PDF.",
        "**2. Structured Ingestion:** The script populates Neo4j with `:College`, `:Department`, and `:Person` nodes from the JSON.",
        "**3. Unstructured Ingestion:** The entire PDF is chunked into `:Chunk` nodes with vector embeddings, and a spaCy NER process links them to `:Person` nodes."
    ]
    for step in pipeline_steps:
        st.markdown(f"<div class='source-card' style='border-left-color: #0033A0;'>{step}</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()