FROM conda/miniconda3
COPY environment.yml /app/

WORKDIR /app
# create environment
RUN conda env create -f environment.yml

## Set envs for Conda Activate (sourcing and `conda activate` won't stick around for the CMD)
ENV PATH='/usr/local/envs/conda-parser/bin:/usr/local/condabin:/opt/conda/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin'
ENV CONDA_PREFIX='/usr/local/envs/conda-parser'
ENV CONDA_SHLVL='1'
ENV CONDA_DEFAULT_ENV='conda-parser'
ENV CONDA_PROMPT_MODIFIER='(conda-parser) '
ENV CONDA_EXE='/usr/local/bin/conda'
ENV _CE_M=''
ENV _CE_CONDA=''
ENV CONDA_PYTHON_EXE='/usr/local/bin/python'
ENV FLASK_APP=conda_parser

COPY conda_parser/ /app/conda_parser
COPY gunicorn_start.sh /app/gunicorn_start.sh

# The fun part
CMD ["./gunicorn_start.sh"]
