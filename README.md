# Down to the Ground (DttG) Database and Tool

## Overview
The **Down to the Ground (DttG) Database** is an open-access research tool designed to support the large-scale study of **colored ground layers in Netherlandish painting (1550–1650)**.  

It was developed as part of the NWO-funded *Down to the Ground* project (2019–2024) and is now hosted by the **RKD – Netherlands Institute for Art History**.  

The tool transforms what began as a single Excel spreadsheet into a **relational database and interactive Django application**. It allows users to browse, query, and export data dynamically, supporting comparative research that would be difficult or impossible with static spreadsheets.  

- Online database: [downtotheground.rkdstudies.nl](https://downtotheground.rkdstudies.nl)  
- Source code: [GitHub Repository](https://github.com/TAHPaul/DttG_db)  
- Documentation: see [`./docs/DttG_Documentation.pdf`](./docs/DttG_Documentation.pdf)  

---

## Project Aims
- Provide the **first large-scale overview** of Netherlandish colored grounds, integrating published, unpublished, and new research.  
- Ensure **data consistency and comparability** through controlled vocabularies (RKDArtists for names, custom color and reliability systems).  
- Create an **open, sustainable infrastructure** for technical art history data, built on widely used frameworks.  
- Offer a **reusable template** for other projects in art history and heritage science (e.g. pigment studies, conservation treatments, iconography).  

---

## Database Architecture
The DttG database is a **relational database** with six core tables:  

- **Artists**  
- **Artworks**  
- **Museums**  
- **Cities**  
- **Data** (technical observations of ground layers)  
- **Colours** (custom classification system for ground color)  

Relationships between tables are maintained using primary and foreign keys. Data normalization ensures consistency (e.g. each artist appears only once, linked to multiple artworks).  

---

## The Django Tool
The web application was built with **Django**, a high-level Python framework for database-driven websites.  

- **Models** mirror the database tables and define relationships.  
- **Templates** are HTML layouts that dynamically generate detail pages for artworks, artists, museums, and cities.  
- **Querying** is supported through both simple and advanced search interfaces, with results exportable as CSV.  
- **Admin**: Django’s built-in admin interface allows secure editing and review of records.  

---

## Contributing Data
We welcome collaboration with researchers and institutions holding information on preparatory layers.  

To contribute:  
1. Download the [Excel input template](./docs/DttG_Submission_Template.xlsx).  
2. Fill in the **Artworks** and **Data** sheets (use the **Colours** and **Reliability rating** tabs for guidance).  
3. Submit completed sheets to:  
   - hall-aquitania@rkd.nl  
   - dttg@rkd.nl  

The DttG team reviews submissions quarterly, ensuring consistency and completeness before integrating new records.  

---

## Reusing the Code
The DttG codebase is intended as a **template for similar projects**.  

- Core models (**Artists, Artworks, Museums, Cities**) apply broadly to art historical datasets.  
- Project-specific models (e.g. **Colours, Data**) can be modified or replaced to suit other research needs.  
- Example: a database on **18th-century Italian conservation treatments** could retain the existing artwork models while replacing the colour system with treatment categories.  
- The same architecture is already being reused in a project on the use and identification of **smalt in Early Modern painting**.  

If you would like to adapt the tool:  
- See the [Documentation PDF](./docs/DttG_Documentation.pdf) for setup instructions.  
- Consult the [Django Documentation](https://docs.djangoproject.com/en/stable/) for further development.  
- Numerous online tutorials are available for beginners—Django’s learning curve is relatively gentle, and the DttG tool was built after two months of self-teaching with limited prior Python experience.  

---

## Using the Database Locally
For researchers wishing to run the tool themselves:  

### Requirements
- Python 3.9+  
- Django  
- Pillow  
- django-crispy-forms  
- django-extensions  
- django-filter  
- django-htmx  

### Setup
```bash
# Clone the repository
git clone https://github.com/TAHPaul/DttG_db.git
cd DttG_db

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate   # on Mac/Linux
venv\Scripts\activate      # on Windows

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver
---
```
## Publications
For full accounts of the methodological and art historical context:  

- Hall-Aquitania, M. & Van Laar, P.J.C. (forthcoming). *Under the Microscope and Into the Database: Designing Data Frameworks for (Technical) Art Historical Research*. *Journal of Historians of Netherlandish Art*.  
- Hall-Aquitania, M. (2025). *Common Grounds: The Introduction and Spread of Coloured Grounds in the Netherlands 1500–1650*. PhD thesis, University of Amsterdam.  
- Hall-Aquitania, M. & Van Laar, P.J.C. (forthcoming). *Down to the Ground: Coloured Grounds in Netherlandish Painting, 1550–1650*. RKD Studies.  

---

## Acknowledgements
This project was developed within the NWO-funded *Down to the Ground* project (2019–2024). It is hosted by the **RKD – Netherlands Institute for Art History**.  

We gratefully acknowledge the support of the **Netherlands Organisation for Scientific Research (NWO)**, the RKD, and the University of Amsterdam.  

Special thanks to the project team, collaborating conservators and conservation scientists, and the many institutions who provided access to paintings and data.  

---

## License
This project is released under the [MIT License](./LICENSE.md).  
You are free to use, copy, modify, and distribute the code, provided the original copyright notice is included.  
The software is provided *as is*, without warranty of any kind.  

---