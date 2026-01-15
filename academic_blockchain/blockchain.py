import hashlib
import datetime


class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        """Membuat blok pertama (Genesis Block) dengan ID = 1"""
        genesis_block = {
            "block_id": 1,
            "student_id": "GENESIS",
            "nama_mahasiswa": "Genesis Block",
            "mata_kuliah": "N/A",
            "nilai": "N/A",
            "semester": 0,
            "dosen_pengampu": "System",
            "tanggal": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "prev_hash": "0",
            "current_hash": self.calculate_hash(1, "GENESIS", "Genesis Block", "N/A", "N/A", 0, "System", "0")
        }
        self.chain.append(genesis_block)

    def calculate_hash(self, block_id, student_id, nama_mahasiswa, mata_kuliah, nilai, semester, dosen_pengampu, prev_hash):
        """Menghitung hash dari data blok"""
        block_string = (
            f"{block_id}"
            f"{student_id}"
            f"{nama_mahasiswa}"
            f"{mata_kuliah}"
            f"{nilai}"
            f"{semester}"
            f"{dosen_pengampu}"
            f"{prev_hash}"
        )
        return hashlib.sha256(block_string.encode()).hexdigest()

    def get_last_block(self):
        """Mendapatkan blok terakhir"""
        return self.chain[-1]

    def create_block(self, student_id, nama_mahasiswa, mata_kuliah, nilai, semester, dosen_pengampu):
        """Membuat blok baru"""
        last_block = self.get_last_block()
        new_block_id = last_block["block_id"] + 1
        prev_hash = last_block["current_hash"]
        tanggal = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        current_hash = self.calculate_hash(
            new_block_id,
            student_id,
            nama_mahasiswa,
            mata_kuliah,
            nilai,
            semester,
            dosen_pengampu,
            prev_hash
        )

        new_block = {
            "block_id": new_block_id,
            "student_id": student_id,
            "nama_mahasiswa": nama_mahasiswa,
            "mata_kuliah": mata_kuliah,
            "nilai": nilai,
            "semester": semester,
            "dosen_pengampu": dosen_pengampu,
            "tanggal": tanggal,
            "prev_hash": prev_hash,
            "current_hash": current_hash
        }

        self.chain.append(new_block)
        return new_block

    def is_chain_valid(self):
        """Memvalidasi integritas blockchain"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            prev_block = self.chain[i - 1]

            # Cek apakah prev_hash sesuai
            if current_block["prev_hash"] != prev_block["current_hash"]:
                return False

            # Recalculate hash dan bandingkan
            recalculated_hash = self.calculate_hash(
                current_block["block_id"],
                current_block["student_id"],
                current_block["nama_mahasiswa"],
                current_block["mata_kuliah"],
                current_block["nilai"],
                current_block["semester"],
                current_block["dosen_pengampu"],
                current_block["prev_hash"]
            )

            if current_block["current_hash"] != recalculated_hash:
                return False

        return True