# 🌿 Environmental Impact Assessment Tool 🌍

Welcome to the Environmental Impact Assessment Tool! 
This project uses Streamlit to create an interactive application that evaluates and presents data related to the environmental impact of various infrastructures. 🚀

I've taken advantage from the terrible event in Valencia caused by the DANA last October 2024. As we know, not 

The data have been collected from [IGN (Insituto Geografico Nacional)](http://www.ign.es/). All the data collected from shapefiles have been processed with ArcGIS, taking just all the information I wanted for this purpose. After that, I exported and processed as ETL pipeline all the data refered to the study area, filtering, fixing and organasing. 

The goal of this project is create a machine learning model, where you can check out if you are living or buying a property in a flow risk area. Mahine Learning model is still not implemented, Im working on that but the key 🔑 is the [DTM (Digital Terrain Model](https://en.wikipedia.org/wiki/Digital_elevation_model). As you know water always find the best ways to flow, so DTM working with ML could show you up very interesting results even if you modify the terrain in a construction project.

So far, the parameters what I choose for work are:
- Roads
- Buildings
- Rivers
- Public transport (railway...)
- Land Cover
- Spanish Cadastre

## 🌟 Features

- 📈 Histograms:
   - Distribution of distance from buildings and roads to nearest water cover.
   - Distribution of affected areas by land cover.
   - Also, the number of buildings that could be affected less than a 1000m 

- 🏢 Buildings:
   - Interactive map where you can choose the town and check out what buildings are affected or not.
   - Labels. You can check the cadastral reference and the mean distance from the nearest river.
     
- 🛣️ Roads:
   - You can filter for highway/freeway, secondary roads, paths, bike paths.
   - See the length affected for the flows and mean distance to the nearest river.
     
- 🧱 Affected Soils: Examine how projects affect the land.
  
- 🌐 SQL Management: Manage databases and users.

- 📦 Queries pre-defined
  
##  🎨 Style and Design

The project includes a custom styling module to give it a modern and professional look, utilizing CSS and auxiliary functions.
