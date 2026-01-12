# **Welcome to the Osteoarthritis (OA) Clustering Feedback App**
This app is designed to help us **evaluate and refine how knee X-ray samples are grouped into clusters** based on their similarity and severity.  
Your feedback helps us understand whether the clustering results make sense visually and clinically, and how we can improve future models.

---

## How it works
You'll find three main sections in the sidebar:

1. **Home Page** - This is where you are now.
2. **Embedding Explorer** - Compare samples and rate how similar or different they appear.  
3. **Cluster Gallery** – Look more closely at all images within each cluster to see if you notice consistent patterns or differences.

Each section includes **simple step-by-step instructions** to guide you.  
When you open a **feedback form**, the relevant **instructions will also be shown directly on the page** — so you can follow along easily as you go.

## Short Introduction
This application presents a new, data-driven way of identifying subgroups in knee osteoarthritis (OA) that go beyond the traditional Kellgren–Lawrence (KL) grading system. Instead of relying on radiographic severity alone, the clustering was derived entirely from patient-reported questionnaire data and clinical patient information.

The goal is to uncover alternative patterns in OA, based on symptoms, function, and lived experience, that may reveal disease subtypes not captured by KL scores.

To support interpretation, corresponding knee X-rays are displayed alongside the clusters. These images are not used to generate the clusters themselves; rather, they give the user a visual reference to compare radiographic appearance with the symptom-based groups.

Technically, the workflow uses UMAP for dimensionality reduction and HDBSCAN for unsupervised clustering. This combination allows complex, high-dimensional questionnaire data to be projected into a meaningful structure and grouped into robust, data-driven clusters.