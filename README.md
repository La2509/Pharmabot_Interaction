# 💊 Pharmabot: Verificador de Interações Medicamentosas

> **Um assistente inteligente para identificar riscos na combinação de fármacos.**

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Status](https://img.shields.io/badge/Status-Em_Desenvolvimento-yellow)
![Focus](https://img.shields.io/badge/Focus-HealthTech-red)

## 🎯 O Problema
A polifarmácia (uso de muitos medicamentos) é um risco real, especialmente para idosos. Interações perigosas podem anular efeitos de remédios ou causar toxicidade grave.

## 💡 A Solução
O **Pharmabot** é uma ferramenta desenvolvida em Python para:
* Receber uma lista de medicamentos do usuário.
* Cruzar dados farmacológicos (em desenvolvimento).
* Alertar sobre interações conhecidas (ex: *Anti-inflamatórios* + *Anticoagulantes*).

## 🛠️ Tecnologias Usadas
* **Linguagem:** Python
* **Interface:** Streamlit
* **Dados:** Pandas (Manipulação de dados)

## 🚀 Como Rodar
```bash
pip install -r requirements.txt
streamlit run pharmabot.py