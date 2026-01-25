# Book-recommender-system-collab-filtering

## Workflow

**Development Order:**

1. `config.yaml` → Define configurations
2. `entity/config_entity.py` → Create config data classes
3. `config/configuration.py` → Build configuration manager
4. `components/stage_XX_*.py` → Implement pipeline stages
5. `pipeline/training_pipeline.py` → Orchestrate all stages
6. `main.py` → Run training pipeline
7. `app.py` → Deploy model for predictions

**To run:**
```bash
python main.py  # Train the model
python app.py   # Run the web app
```

# Setup Instructions

## Clone the Repository
```bash
git clone https://github.com/entbappy/End-to-End-Book-Recommender-System.git
cd End-to-End-Book-Recommender-System
```

## Step 1: Create and Activate Conda Environment
```bash
conda create -n books python=3.7.10 -y
conda activate books
```

## Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

## Step 3: Run the Application
```bash
streamlit run app.py
