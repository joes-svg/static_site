import os
import sys
from markdown_blocks import markdown_to_html_node  # Assuming you have a module for this conversion

def extract_title(markdown_file):
    """
    Extracts the title from a markdown file. The title is assumed to be the first line that starts with '# '.
    """
    with open(markdown_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('# '):
                return line[2:].strip()  # Remove the '# ' and strip whitespace
    raise ValueError("No title found in the markdown file")

def generate_page(from_path, template_path, output_path):
    """
    Generates an HTML page from a markdown file using a template.
    """
    
    title = extract_title(from_path)
    
    # Read the markdown content
    with open(from_path, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
        
    title = extract_title(from_path)
    
    # Read the template content
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()

    # Replace placeholders in the template
    html_content = template_content.replace('{{ Title }}', title)
    html_content = html_content.replace('{{ Content }}', markdown_to_html_node(markdown_content).to_html()) 
    # html_content = html_content.replace('href="/', f'href="{from_path}/')
    # html_content = html_content.replace('src="/', f'src="{from_path}/')
    
    # Write the generated HTML to the output path
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Stage 1: Generating pages from '{from_path}' to '{output_path}' using template '{template_path}'")

def copy_directory_recursively(source_dir, destination_dir):
    """
    Recursively copies all contents from source_dir to destination_dir without shutil.
    """
    
    # Create the destination directory if it doesn't exist
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    # Iterate over all items in the source directory
    for item in os.listdir(source_dir):
        source_item_path = os.path.join(source_dir, item)
        destination_item_path = os.path.join(destination_dir, item)

        # Check if the item is a file or a directory
        if os.path.isfile(source_item_path):
            # Copy the file
            with open(source_item_path, 'rb') as f_src:
                with open(destination_item_path, 'wb') as f_dst:
                    # Read and write in chunks to handle large files efficiently
                    while True:
                        chunk = f_src.read(4096)
                        if not chunk:
                            break
                        f_dst.write(chunk)
        
        elif os.path.isdir(source_item_path):
            # Recursively call the function for subdirectories
            copy_directory_recursively(source_item_path, destination_item_path)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    """
    Recursively generates HTML pages from markdown files in a directory structure.
    """
    for item in os.listdir(dir_path_content):
        source_item_path = os.path.join(dir_path_content, item)
        destination_item_path = os.path.join(dest_dir_path, item)

        if os.path.isfile(source_item_path) and source_item_path.endswith('.md'):
            # Generate the corresponding HTML file path
            html_file_name = os.path.splitext(item)[0] + '.html'
            output_html_path = os.path.join(dest_dir_path, html_file_name)
            generate_page(source_item_path, template_path, output_html_path)
        
        elif os.path.isdir(source_item_path):
            # Create the corresponding directory in the destination
            if not os.path.exists(destination_item_path):
                os.makedirs(destination_item_path)
            # Recursively process the subdirectory
            generate_pages_recursive(source_item_path, template_path, destination_item_path)    
    
def main():
    if len(sys.argv) > 1:
        basepath = f'{sys.argv[1]}/'
    else:
        basepath = ""
    
    source_directory = "static"
    destination_directory = f"{basepath}docs"
    generate_pages_recursive("content", "template.html", destination_directory)
    # generate_page("content/index.md", "template.html", "public/index.html")
    # generate_page("content/blog/glorfindel/index.md", "template.html", "public/blog/glorfindel/index.html")
    # generate_page("content/blog/tom/index.md", "template.html", "public/blog/tom/index.html")
    # generate_page("content/blog/majesty/index.md", "template.html", "public/blog/majesty/index.html")
    # generate_page("content/contact/index.md", "template.html", "public/contact/index.html")
    copy_directory_recursively(source_directory, destination_directory)
    print(f"Stage 2: Contents of '{source_directory}' have been copied to '{destination_directory}'.")

if __name__ == "__main__":
    main()