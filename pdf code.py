import fitz
from PIL import Image
import io

def process_pdf(input_pdf_path, output_pdf_path, top_fraction=0.2, right_fraction=0.1):
    document = fitz.open(input_pdf_path)
    
    new_document = fitz.open()

    for page_number in range(len(document)):
        page = document.load_page(page_number)

        width, height = page.rect.width, page.rect.height

        crop_area = fitz.Rect(0, height / 2, width, height)

        cropped_pixmap = page.get_pixmap(clip=crop_area, dpi=300)

        image = Image.frombytes(
            "RGB", 
            (cropped_pixmap.width, cropped_pixmap.height), 
            cropped_pixmap.samples
        )

        img_width, img_height = image.size

        right_crop = int(img_width * right_fraction)
        top_crop = int(img_height * top_fraction)

        cropped_image = image.crop(
            (
                0,
                top_crop,
                img_width - right_crop,
                img_height
            )
        )

        rotated_image = cropped_image.rotate(90, expand=True)

        rotated_width, rotated_height = rotated_image.size

        new_page = new_document.new_page(width=rotated_width, height=rotated_height)

        img_buffer = io.BytesIO()
        rotated_image.save(img_buffer, format='PNG')

        new_page.insert_image(
            fitz.Rect(0, 0, rotated_width, rotated_height),
            stream=img_buffer.getvalue()
        )

    new_document.save(output_pdf_path)
    new_document.close()
    document.close()


input_pdf = 'unprocessedlabels.pdf'
output_pdf = 'processedlabels.pdf'

process_pdf(input_pdf, output_pdf, top_fraction=0.2, right_fraction=0.1)

print("PDF processed and saved as 'processed_shipping_labels_cropped.pdf'")