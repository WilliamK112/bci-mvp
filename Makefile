.PHONY: setup check train api demo benchmark ensemble cross coral explain shap docker-build docker-run

setup:
	python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt

check:
	python src/check_data.py

train:
	python src/train.py

api:
	uvicorn api.main:app --reload --port 8000

demo:
	streamlit run app/dashboard.py

benchmark:
	python src/benchmark.py

ensemble:
	python src/ensemble_benchmark.py

cross:
	python src/cross_dataset_eval.py --train dataset_a --test dataset_b

coral:
	python src/cross_dataset_coral.py

explain:
	python src/explainability.py

shap:
	python src/shap_explain.py

docker-build:
	docker build -t bci-mvp:latest .

docker-run: docker-build
	docker run -p 8000:8000 -v $(PWD)/outputs:/app/outputs bci-mvp:latest

test:
	python -m unittest discover -s tests -p "*_unittest.py"

full:
	python src/run_full_pipeline.py
