import json
from pathlib import Path
from typing import Any, Dict, List


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_FILE = DATA_DIR / "database.json"


def _seed() -> Dict[str, Any]:
    return {
        "counters": {"users": 4, "items": 4, "requests": 3},
        "users": [
            {
                "id": 1,
                "name": "Gabriel Doador",
                "email": "doador@solidario.org",
                "password_hash": "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92",
                "role": "donor",
                "region": "Centro",
                "x": 2.0,
                "y": 4.0,
            },
            {
                "id": 2,
                "name": "Maria Beneficiaria",
                "email": "beneficiaria@solidario.org",
                "password_hash": "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92",
                "role": "beneficiary",
                "region": "Zona Norte",
                "x": 5.0,
                "y": 8.0,
            },
            {
                "id": 3,
                "name": "ONG Esperanca",
                "email": "ong@solidario.org",
                "password_hash": "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92",
                "role": "organization",
                "region": "Zona Sul",
                "x": 7.0,
                "y": 3.0,
            },
            {
                "id": 4,
                "name": "Jose Beneficiario",
                "email": "jose@solidario.org",
                "password_hash": "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92",
                "role": "beneficiary",
                "region": "Centro",
                "x": 3.5,
                "y": 3.0,
            },
        ],
        "items": [
            {
                "id": 1,
                "title": "Cesta basica",
                "category": "alimentos",
                "quantity": 10,
                "status": "disponivel",
                "donor_id": 1,
                "region": "Centro",
                "x": 2.0,
                "y": 4.0,
            },
            {
                "id": 2,
                "title": "Casacos infantis",
                "category": "roupas",
                "quantity": 6,
                "status": "disponivel",
                "donor_id": 3,
                "region": "Zona Sul",
                "x": 7.0,
                "y": 3.0,
            },
            {
                "id": 3,
                "title": "Kit higiene",
                "category": "higiene",
                "quantity": 12,
                "status": "reservado",
                "donor_id": 1,
                "region": "Centro",
                "x": 2.0,
                "y": 4.0,
            },
            {
                "id": 4,
                "title": "Leite em po",
                "category": "alimentos",
                "quantity": 8,
                "status": "entregue",
                "donor_id": 3,
                "region": "Zona Sul",
                "x": 7.0,
                "y": 3.0,
            },
        ],
        "requests": [
            {
                "id": 1,
                "beneficiary_id": 2,
                "category": "alimentos",
                "description": "Familia com necessidade de alimentos.",
                "needed_quantity": 4,
                "status": "aberta",
                "region": "Zona Norte",
                "x": 5.0,
                "y": 8.0,
            },
            {
                "id": 2,
                "beneficiary_id": 4,
                "category": "roupas",
                "description": "Necessidade de roupas para criancas.",
                "needed_quantity": 2,
                "status": "aberta",
                "region": "Centro",
                "x": 3.5,
                "y": 3.0,
            },
            {
                "id": 3,
                "beneficiary_id": 2,
                "category": "higiene",
                "description": "Itens de higiene pessoal.",
                "needed_quantity": 3,
                "status": "atendida",
                "region": "Zona Norte",
                "x": 5.0,
                "y": 8.0,
            },
        ],
    }


def ensure_data_file() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not DATA_FILE.exists():
        DATA_FILE.write_text(json.dumps(_seed(), ensure_ascii=True, indent=2), encoding="utf-8")


def load_data() -> Dict[str, Any]:
    ensure_data_file()
    return json.loads(DATA_FILE.read_text(encoding="utf-8"))


def save_data(data: Dict[str, Any]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(json.dumps(data, ensure_ascii=True, indent=2), encoding="utf-8")


def next_id(data: Dict[str, Any], key: str) -> int:
    data["counters"][key] += 1
    return data["counters"][key]


def filter_by_region(records: List[Dict[str, Any]], region: str) -> List[Dict[str, Any]]:
    if not region:
        return records
    return [record for record in records if record.get("region", "").lower() == region.lower()]
