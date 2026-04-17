import os

def load_knowledge(folder_path):
    knowledge_text = ""

    if not os.path.exists(folder_path):
        print(f"⚠️ Carpeta {folder_path} no existe")
        return ""

    for filename in os.listdir(folder_path):
        if filename.endswith(".md"):
            file_path = os.path.join(folder_path, filename)

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    knowledge_text += f"\n\n--- {filename} ---\n\n"
                    knowledge_text += content
            except Exception as e:
                print(f"Error leyendo {filename}: {e}")

    print("✅ Conocimiento cargado correctamente")
    return knowledge_text