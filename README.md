# 🌿 Environmental Impact Assessment Tool 🌍

Welcome to the Environmental Impact Assessment Tool! 
This project uses Streamlit to create an interactive application that evaluates and presents data related to the environmental impact of various infrastructures. 🚀

I have taken this project as an opportunity to analyze the devastating DANA event that struck Valencia in October 2024. As we know, not all areas were equally affected, and understanding these patterns is crucial for future risk assessment and mitigation.

The data have been collected from 🌍[IGN (Insituto Geografico Nacional)](http://www.ign.es/). All the data collected from shapefiles have been processed with ArcGIS, taking just the information I wanted for this purpose. After that, I exported it and processed as an ETL pipeline, cleaning, filtering, fixing and organizing it. 

The goal of this project is create a machine learning model,allowing you to check if you are living or buying a property in a flood risk area. Machine Learning model is still not implemented, Im working on that but the key 🔑 is the [DTM (Digital Terrain Model](https://en.wikipedia.org/wiki/Digital_elevation_model). As you know water always find the best ways to flow, so DTM working with ML could show you up very interesting results even if you modify the terrain in a construction project.

So far, the parameters what I choose for work are:
- Roads
- Buildings
- Rivers
- Public transport (railway...)
- Land Cover
- Spanish Cadastre

## 🌟 Features

- 📈 Histograms:
   - Distribution of distances from buildings and roads to nearest water cover.
   - Distribution of affected areas by land cover.
   - Also, the number of buildings that could be affected within 1000m 

- 🏢 Buildings:
   - Interactive map where you can choose the town and check out which buildings are affected or not.
   - Labels. You can check the cadastral reference and the average distance from the nearest river.
     
- 🛣️ Roads:
   - Filter by highway/freeway, secondary roads, paths, and bike paths.
   - See the length affected for the flood and average distance to the nearest river.
     
- 🧱 Affected Soils: Examine which soils have been affected.
  
- 🌐 SQL Management: Manage databases and users.

- 📦 Predefined queries
  
##  🎨 Style and Design

The project includes a custom styling module to enhance its modern and professional look, utilizing CSS and auxiliary functions.


