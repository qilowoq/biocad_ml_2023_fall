Репозиторий с решением задания на стажировку в компанию BIOCAD в команду машинного обучения.

Готовый продукт представлен в streamlit приложении. Запустить его можно командой:

```shell
streamlit run streamlit_app.py
```

Для запуска потребуется создать виртуальное окружение и установить зависимости:

```shell
conda create --name biocad-ml-env python=3.11
conda activate biocad-ml-env
pip install -r requirements.txt
```

Альтернативой является использование [Dockerfile](Dockerfile)

* `docker build -t ml-biocad-image .`

* Запускаем контейнер, прикрепляем к нему папку с репозиторием и запускаем streamlit приложение
```shell
docker run -it --name ml-biocad-cont -v ПУТЬ_ДО_ПАПКИ_С_КОДОМ:/ml ml-biocad-image
cd /ml
streamlit run streamlit_app.py --server.port=8501 --server.address=0.0.0.0
```