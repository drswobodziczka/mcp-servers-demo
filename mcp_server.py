from mcp.server.fastmcp import FastMCP
from pydantic import Field
from mcp.server.fastmcp.prompts import base

### MCP SERVER -- by FastMCP ###
mcp = FastMCP("DocumentMCP", log_level="ERROR")

### MCP internal database ###
docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}

### MCP TOOLS ###
@mcp.tool(
    name="read_document",
    description="Reads the contents of a document and returns as a string.",
)
def read_doc(doc_id: str = Field(description="The ID of the document to read.")) -> str:
    return docs[doc_id]

@mcp.tool(
    name="edit_document",
    description="Edits the contents of a document by replacing the old content with the new string.",
)
def edit_doc(
    doc_id: str = Field(description="The ID of the document to edit."),
    old_content: str = Field(description="The text to replace in the document, must match the exactly including whitespaces."),
    new_content: str = Field(description="The new content to be inserted instead of the old content .")
    ):
    docs[doc_id] = docs[doc_id].replace(old_content, new_content)    

### MCP RESOURCES ###
@mcp.resource(
    uri="docs://documents",
    description="Returns a list of document IDs.",
    mime_type="application/json",
)
def list_docs_ids():
    return list(docs.keys())

@mcp.resource(
    uri="docs://documents/{doc_id}",
    description="Returns the contents of a document.",
    mime_type="text/plain",
)
def get_doc_content(doc_id: str):
    return docs[doc_id] 

### MCP PROMPTS ###
@mcp.prompt(
    name="format",
    description="Formats the contents of a document in markdown format and returns as a string.",
)
def rewrite_doc(doc_id: str = Field(description="The ID of the document to format.")) -> list[base.Message]: 
    prompt = f"""
    
    Your goal is to reformat the document into markdown.
    
    Id of document you need to reformat is: 
    
    <document_id>
    {doc_id}
    </document_id>
    
    NOTE: USE 'edit_document' tool to edit the document. 
    NOTE: Do NOT change the text - just reformat it.
    
    Return final result of the document to the user!
    
    """
    return  [ 
             base.UserMessage(prompt) 
    ]

# TODO: Write a prompt to summarize a doc

if __name__ == "__main__":
    mcp.run(transport="stdio")
