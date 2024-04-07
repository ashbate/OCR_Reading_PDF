<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/ashbate/OCR_Reading_PDF">
    <img src="/visuals/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">OCR Reading PDF</h3>

  <p align="center">
    An innovative library designed to segment column-based layouts in PDFs into manageable snippets, enhancing OCR (Optical Character Recognition) processes.
    <br />
    <a href="https://github.com/ashbate/OCR_Reading_PDF"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/ashbate/OCR_Reading_PDF">View Demo</a>
    ·
    <a href="https://github.com/ashbate/OCR_Reading_PDF/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/ashbate/OCR_Reading_PDF/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

## About The Project

OCR Reading PDF is designed to enhance the preprocessing steps for OCR applications, particularly focusing on PDFs with newspaper-style column-based layouts. It employs advanced image processing to segment pages into columns or snippets, significantly improving subsequent OCR accuracy.

### Built With

* [Pillow](https://python-pillow.org)
* [pdf2image](https://pypi.org/project/pdf2image/)
* [NumPy](https://numpy.org)
* [Pandas](https://pandas.pydata.org)

## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

Ensure you have Python 3.6 or later installed on your system.

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/ashbate/OCR_Reading_PDF.git

2. Navigate to the cloned directory and install required packages:
   ```sh
   pip install -r requirements.txt

### Usage

For detailed usage instructions, please refer to the [Documentation](https://github.com/ashbate/OCR_Reading_PDF).

## Usage

The library processes scanned PDF files of newspaper-style columnar documents, breaking them down into individual column images for enhanced OCR accuracy. Here's a step-by-step guide using the provided methods:

1. **Convert the PDF to Image**: Begin by converting your PDF pages into images. For the sake of this example, we will assume that this step has been completed and we now have images of each page.

2. **Adjust the Image**: Crop the image to eliminate extraneous borders or edges, streamlining the OCR process. Here's the result after using the `adjust` method:

   ![Adjusted Image](/visuals/fullpage.png)

3. **Get Cut Points**: Calculate the precise locations at which the image should be cut into columns or snippets with the `get_cutpoints` method.

4. **Cut the Image into Snippets**: Utilizing the cut points, slice the images into individual columns. Here are the snippets after being processed:

<table>
  <tr>
    <td>
      <img src="/visuals/snippet1.png" alt="Snippet 1" width="300"/>
    </td>
    <td>
      <img src="/visuals/snippet2.png" alt="Snippet 2" width="300"/>
    </td>
    <td>
      <img src="/visuals/snippet3.png" alt="Snippet 3" width="300"/>
    </td>
  </tr>
</table>


5. **Prepare for OCR**: The individual column images are now prepared for OCR processing to extract the textual content.

For a full demonstration, see the examples below created with images from a sample document.



## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project.
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`).
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the Branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Project Link: [https://github.com/ashbate/OCR_Reading_PDF](https://github.com/ashbate/OCR_Reading_PDF)

## Acknowledgments

- Image processing techniques and tools.
- Optical Character Recognition (OCR) technology.
- All contributors and open-source communities.
