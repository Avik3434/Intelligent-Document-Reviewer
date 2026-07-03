import os

def list_pdf():
    pdfs = []
    folder_path = "PDFS" #Paste your own path
    print("--select file--\n")
    for file in os.listdir(folder_path):
        full_path = os.path.join(folder_path, file)

        if os.path.isfile(full_path) and file.lower().endswith(".pdf"):
            pdfs.append(file)

    for i, pdf in enumerate(pdfs, start=1):
        print(f"{i}. {pdf}")

    while True:
        try:
            
            choice = int(input("\nEnter the number of the PDF you want to choose: "))

            if 1 <= choice <= len(pdfs):
                selected = os.path.join(folder_path, pdfs[choice - 1])
                print(f"Selected: {pdfs[choice - 1]}\n")
                return selected

            print("Invalid number. Try again.")

        except ValueError:
            print("Please enter a valid number.")

if __name__ == "__main__":
    print(list_pdf())