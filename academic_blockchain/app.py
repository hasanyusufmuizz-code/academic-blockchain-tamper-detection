from flask import Flask, request, jsonify
from blockchain import Blockchain
import requests
import hashlib

app = Flask(__name__)

# Config
GOOGLE_SHEET_URL = "https://script.google.com/macros/s/AKfycbx3gAFwJibYjO8hyS4cqEmH2cUqN_6w1mf6khFPHXscRK_1oF7pRygR-T8PFrjuugfT/exec"

blockchain = Blockchain()


def hash_cloud_data(row):
    """Hash data dari Google Sheets untuk perbandingan"""
    block_string = (
        f"{row['block_id']}"
        f"{row['student_id']}"
        f"{row['nama_mahasiswa']}"
        f"{row['mata_kuliah']}"
        f"{row['nilai']}"
        f"{row['semester']}"
        f"{row['dosen_pengampu']}"
        f"{row['prev_hash']}"
    )
    return hashlib.sha256(block_string.encode()).hexdigest()


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Flask Academic Blockchain API is running",
        "endpoints": {
            "POST /add_data": "Tambah data nilai mahasiswa",
            "GET /get_chain": "Lihat seluruh blockchain",
            "GET /verify_chain": "Verifikasi integritas blockchain",
            "GET /detect_cloud_tampering": "Deteksi manipulasi di Google Sheets",
            "POST /init_demo_data": "Inisialisasi 4 blok demo untuk Case 3"
        }
    })


# POST /init_demo_data - Untuk memenuhi minimal 4 blok Case 3
@app.route("/init_demo_data", methods=["POST"])
def init_demo_data():
    """Membuat 4 blok sesuai skenario Case 3"""
    demo_blocks = [
        {
            "student_id": "MHS-2023-001",
            "nama_mahasiswa": "Budi Santoso",
            "mata_kuliah": "Kriptografi",
            "nilai": "B+",
            "semester": 5,
            "dosen_pengampu": "Dr. Lina",
            "description": "Input nilai UTS"
        },
        {
            "student_id": "MHS-2023-001",
            "nama_mahasiswa": "Budi Santoso",
            "mata_kuliah": "Kriptografi",
            "nilai": "A",
            "semester": 5,
            "dosen_pengampu": "Dr. Lina",
            "description": "Input nilai UAS"
        },
        {
            "student_id": "MHS-2023-001",
            "nama_mahasiswa": "Budi Santoso",
            "mata_kuliah": "Kriptografi",
            "nilai": "A",
            "semester": 5,
            "dosen_pengampu": "Dr. Lina",
            "description": "Finalisasi mata kuliah"
        },
        {
            "student_id": "MHS-2023-001",
            "nama_mahasiswa": "Budi Santoso",
            "mata_kuliah": "Sertifikat Kriptografi",
            "nilai": "LULUS",
            "semester": 5,
            "dosen_pengampu": "Dr. Lina",
            "description": "Penerbitan sertifikat"
        }
    ]

    created_blocks = []

    for demo in demo_blocks:
        block = blockchain.create_block(
            demo["student_id"],
            demo["nama_mahasiswa"],
            demo["mata_kuliah"],
            demo["nilai"],
            demo["semester"],
            demo["dosen_pengampu"]
        )

        # Kirim ke Google Sheets
        try:
            requests.post(GOOGLE_SHEET_URL, json=block)
        except Exception as e:
            return jsonify({
                "error": f"Gagal mengirim blok {block['block_id']} ke Google Sheets",
                "detail": str(e)
            }), 500

        created_blocks.append({
            "block_id": block["block_id"],
            "description": demo["description"],
            "nilai": block["nilai"]
        })

    return jsonify({
        "message": "Demo data berhasil dibuat (4 blok Case 3)",
        "blocks": created_blocks,
        "total_blocks": len(blockchain.chain),
        "note": "Genesis block (ID=1) + 4 blok data = 5 blok total"
    }), 201


# POST /add_data
@app.route("/add_data", methods=["POST"])
def add_data():
    data = request.json

    required_fields = [
        "student_id",
        "nama_mahasiswa",
        "mata_kuliah",
        "nilai",
        "semester",
        "dosen_pengampu"
    ]

    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Field '{field}' tidak ditemukan"}), 400

    # Buat block di blockchain
    block = blockchain.create_block(
        data["student_id"],
        data["nama_mahasiswa"],
        data["mata_kuliah"],
        data["nilai"],
        data["semester"],
        data["dosen_pengampu"]
    )

    # Kirim ke Google Sheets
    try:
        requests.post(GOOGLE_SHEET_URL, json=block)
    except Exception as e:
        return jsonify({
            "error": "Gagal mengirim ke Google Sheets",
            "detail": str(e)
        }), 500

    return jsonify({
        "message": "Data berhasil ditambahkan",
        "block": block
    }), 201


# GET /get_chain
@app.route("/get_chain", methods=["GET"])
def get_chain():
    return jsonify({
        "length": len(blockchain.chain),
        "chain": blockchain.chain
    })


# GET /verify_chain
@app.route("/verify_chain", methods=["GET"])
def verify_chain():
    valid = blockchain.is_chain_valid()
    
    result = {
        "valid": valid,
        "message": "✅ Blockchain VALID - Tidak ada manipulasi" if valid else "❌ Blockchain TIDAK VALID - Terdeteksi manipulasi!",
        "total_blocks": len(blockchain.chain)
    }

    if not valid:
        result["warning"] = "Data telah diubah! Periksa integritas blok."

    return jsonify(result)


# GET /detect_cloud_tampering
@app.route("/detect_cloud_tampering", methods=["GET"])
def detect_cloud_tampering():
    try:
        # Ambil data dari Google Sheets
        response = requests.get(GOOGLE_SHEET_URL)
        cloud_data = response.json()

        tampered = False
        details = []

        # Bandingkan setiap blok (skip genesis block)
        for block in blockchain.chain[1:]:
            found = False
            for row in cloud_data:
                if row["block_id"] == block["block_id"]:
                    found = True
                    recalculated_hash = hash_cloud_data(row)

                    if recalculated_hash != block["current_hash"]:
                        tampered = True
                        details.append({
                            "block_id": block["block_id"],
                            "student_id": block["student_id"],
                            "status": "⚠️ DATA TAMPERED",
                            "blockchain_nilai": block["nilai"],
                            "cloud_nilai": row["nilai"],
                            "blockchain_hash": block["current_hash"],
                            "cloud_recalculated_hash": recalculated_hash
                        })
                    else:
                        details.append({
                            "block_id": block["block_id"],
                            "student_id": block["student_id"],
                            "status": "✅ VALID"
                        })
                    break

            if not found:
                tampered = True
                details.append({
                    "block_id": block["block_id"],
                    "status": "❌ MISSING FROM CLOUD"
                })

        return jsonify({
            "tampered": tampered,
            "message": "❌ Manipulasi data terdeteksi di Google Sheets!" if tampered else "✅ Data cloud aman dan sesuai blockchain",
            "total_blocks_checked": len(blockchain.chain) - 1,
            "details": details
        })

    except Exception as e:
        return jsonify({
            "error": "Gagal memeriksa cloud",
            "detail": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)