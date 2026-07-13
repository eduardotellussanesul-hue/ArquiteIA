# ArquiteIA

Projeto de integração de Arquitetura de Computadores e Inteligência Artificial.

**Visão geral**

ArquiteIA é um projeto em camadas que combina um núcleo C++ (simulador/estimador),
uma camada Python para treinar/otimizar estratégias, uma API (FastAPI) e integração
com um LMS para visualizações e explicações.

**Estrutura principal**

- `backend_simulator/` - C++ core (simulador de cache, estimadores). Veja [backend_simulator/CMakeLists.txt](backend_simulator/CMakeLists.txt).
- `ai_trainer/` - scripts Python para gerar datasets e treinar otimizadores (`dataset_generator.py`, `optimize_tile.py`).
- `api_orchestrator/` - FastAPI para expor estimativas e modelos (`api_orchestrator/main.py`).
- `lms_integrator/` - ferramentas e visualizações para o LMS (`lms_integrator/visualize.py`).

**Pré-requisitos (Windows)**

- Python 3.8+ (recomendado 3.10/3.11/3.12)
- CMake (>= 3.10; prefira 3.20+)
- Visual Studio com workload "Desktop development with C++" (ou Build Tools com MSVC)
- Git (para FetchContent do pybind11)

Instale dependências Python:

```powershell
py -m pip install -r requirements.txt
```

**Build do módulo C++ (pybind11)**

1. Abra PowerShell x64 Developer (ou configure ambiente do Visual Studio).
2. No diretório do projeto:

```powershell
cd backend_simulator
rd /s /q build
mkdir build
cd build
$pyexe = py -c "import sys;print(sys.executable)"
cmake .. -DCMAKE_BUILD_TYPE=Release -A x64 -DPython_EXECUTABLE="$pyexe"
cmake --build . --config Release
```

Observações:
- Se o CMake reclamar de pybind11/cmake policy, atualize o CMake ou use a opção `-DCMAKE_POLICY_VERSION_MINIMUM=3.5`.
- Se ocorrer erro sobre MSVC antigo, instale/atualize o Visual Studio C++ workload.

Após build o artefato estará em `backend_simulator/build/Release/` (ex.: `arquiteia.cp312-win_amd64.pyd`).

**Executando scripts e API**

- Gerar casos de teste (dataset):

```powershell
py ai_trainer/dataset_generator.py
```

- Rodar o otimizador placeholder:

```powershell
py ai_trainer/optimize_tile.py
```

- Rodar a API (FastAPI):

```powershell
uvicorn api_orchestrator.main:app --reload --host 127.0.0.1 --port 8000
```

**Testar import do módulo C++**

```powershell
# $env:PYTHONPATH = "$(Resolve-Path backend_simulator\build\Release)" + ";$env:PYTHONPATH"
py -c "import arquiteia; print(arquiteia.compute_gemm_flops(8))"
```

**Troubleshooting rápido**

- Erro `pybind11 2.10+ requires MSVC 2017 or newer`: atualize Visual Studio C++ ou ajuste `CMakeLists.txt` para usar uma versão compatível do pybind11.
- Erro `could not find pybind11`: instale `pybind11` via `py -m pip install --user pybind11` ou deixe que o CMake faça o FetchContent (requer Git).
- Erros do IntelliSense no VS Code (ex.: `yvals.h`, `Python.h`): execute `C/C++: Reset IntelliSense Database` e garanta que `.vscode/c_cpp_properties.json` aponte para as includes do MSVC e para `C:/Users/<you>/AppData/Local/Programs/Python/PythonXXX/Include`.

**Arquivos úteis**

- [backend_simulator/CMakeLists.txt](backend_simulator/CMakeLists.txt)
- [backend_simulator/include/arquiteia.hpp](backend_simulator/include/arquiteia.hpp)
- [ai_trainer/dataset_generator.py](ai_trainer/dataset_generator.py)
- [api_orchestrator/main.py](api_orchestrator/main.py)

# 🧠 ArquiteIA

**Arquitetura de Computadores + Inteligência Artificial**

O **ArquiteIA** é um sistema híbrido que combina um simulador de cache de alta performance (escrito em C++) com um agente de Inteligência Artificial (Python/PyTorch) para otimizar a técnica de **Loop Tiling** em multiplicação de matrizes (MatMul). O objetivo é encontrar o tamanho de bloco (Tile Size) ideal que minimize *Cache Misses* para diferentes configurações de hardware e dimensões de matriz.

O sistema é integrado a um **LMS com Tutor IA**, permitindo que o tutor responda perguntas sobre desempenho de hardware com base em simulações reais.

---

## 🏗️ Arquitetura do Sistema

O projeto é dividido em 4 camadas independentes, garantindo baixo acoplamento e alta performance onde ela é mais necessária.

```text
┌─────────────────────────────────────────────────────────────────────┐
│                    CAMADA 4: FRONTEND / LMS                        │
│         (Seu LMS existente + Chat do Tutor IA + Streamlit)         │
│              - Tutor chama a Tool "ArquiteIA" via API              │
└───────────────────────────────┬─────────────────────────────────────┘
                                │ HTTP / JSON
┌───────────────────────────────▼─────────────────────────────────────┐
│                    CAMADA 3: API E ORQUESTRADOR                     │
│                   (Python + FastAPI + SQLite)                      │
│         - Endpoints REST para otimização e simulação               │
│         - Gerencia histórico de execuções                          │
└───────────────────────────────┬─────────────────────────────────────┘
                                │ Chamada nativa (pybind11)
┌───────────────────────────────▼─────────────────────────────────────┐
│                 CAMADA 2: AGENTE DE IA (Python)                    │
│              (PyTorch + Optuna - Otimização Bayesiana)             │
│   - Treina o modelo para prever o melhor Tile Size baseado em:    │
│     [TamanhoMatriz, TamanhoL1, TamanhoL2] -> [Tile Ótimo]         │
└───────────────────────────────┬─────────────────────────────────────┘
                                │ pybind11 (C++ -> Python)
┌───────────────────────────────▼─────────────────────────────────────┐
│              CAMADA 1: MOTOR DE SIMULAÇÃO (C++17)                  │
│   ⚙️  Multiplicação de Matrizes com Loop Tiling (MatMul)          │
│   ⚙️  Simulador de Cache (LRU) contando Hits/Misses              │
│   ⚙️  Estimador de Ciclos (Latência RAM vs. Cache)                │
│   ⚙️  Saída: struct { misses, hits, ciclos_estimados }            │
└─────────────────────────────────────────────────────────────────────┘