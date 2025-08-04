FROM asia-east1-docker.pkg.dev/aftership-admin/ci-artifacts/python-onbuild:python-3.11.7

RUN find cmd -type f -name '*.sh' -exec chmod +x {} \; && \
    pip install uv && \
    uv venv --python 3.11.7 && \
    uv sync

EXPOSE 9080

ENTRYPOINT ["./cmd/run_server.sh"]
