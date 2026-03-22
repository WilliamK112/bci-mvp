.PHONY: setup check train api demo benchmark cross explain docker-build

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

cross:
	python src/cross_dataset_eval.py --train dataset_a --test dataset_b

explain:
	python src/explainability.py

docker-build:
	docker build -t bci-mvp:latest .
