import csv, zipfile, pyodbc, io, os

FILES = ["ES.zip"]
CONN_STR = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=ANIER-PC\\A3ERP;DATABASE=KratosDB;UID=sa;PWD=Asd123$%;TrustServerCertificate=yes"

cnxn = pyodbc.connect(CONN_STR, autocommit=False)
cur = cnxn.cursor()

import pyodbc

class BatchInserter:
    def __init__(self, conn_str, batch_size=2000):
        self.conn = pyodbc.connect(conn_str, autocommit=False)
        self.cur = self.conn.cursor()
        self.cur.fast_executemany = True
        self.batch = []
        self.batch_size = batch_size

    def insert_row(self, cc, postal, place, a1_code, a1_name, a2_code, a2_name, lat, lon, acc):
        self.batch.append((
            cc, postal, place, a1_name, a1_code,
            a2_name, a2_code, None, None,
            float(lat) if lat else None,
            float(lon) if lon else None,
            int(acc) if acc else None
        ))
        if len(self.batch) >= self.batch_size:
            self.flush()

    def flush(self):
        if not self.batch:
            return
        self.cur.executemany("""
            INSERT INTO dbo.POSTAL_CODES
            (COUNTRY_CODE, POSTAL_CODE, PLACE_NAME, ADMIN1_NAME, ADMIN1_CODE,
             ADMIN2_NAME, ADMIN2_CODE, ADMIN3_NAME, ADMIN3_CODE, LATITUDE, LONGITUDE, ACCURACY)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, self.batch)
        self.conn.commit()
        self.batch.clear()

    def close(self):
        self.flush()
        self.cur.close()
        self.conn.close()


def make_insert_row(conn_str):
    def insert_row(cc, postal, place, a1_code, a1_name, a2_code, a2_name, lat, lon, acc):

        print(f"Insertando {cc} {postal} {place}")

        with pyodbc.connect(conn_str) as cn:
            cur = cn.cursor()
            cur.execute("""
                INSERT INTO dbo.POSTAL_CODES
                (COUNTRY_CODE, POSTAL_CODE, PLACE_NAME, ADMIN1_NAME, ADMIN1_CODE,
                 ADMIN2_NAME, ADMIN2_CODE, ADMIN3_NAME, ADMIN3_CODE, LATITUDE, LONGITUDE, ACCURACY)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                cc, postal, place, a1_name, a1_code,
                a2_name, a2_code, None, None,              # admin3 no viene en todos los países
                float(lat) if lat else None,
                float(lon) if lon else None,
                int(acc) if acc else None
            ))
            cn.commit()

            print(f"Insertado {cc} {postal} {place}")
    return insert_row

def load_postal_zip(zip_path, insert_row):
    # country desde el nombre del zip (ES.zip -> ES)
    iso = os.path.splitext(os.path.basename(zip_path))[0][:2].upper()
    with zipfile.ZipFile(zip_path) as zf:
        # suele traer un .txt
        inner = next(n for n in zf.namelist() if n.lower().endswith(('.txt', '.csv')))
        with zf.open(inner) as fh:
            reader = csv.reader(io.TextIOWrapper(fh, 'utf-8'), delimiter='\t')

            print(f"Insertando códigos postales para {iso} desde {zip_path}...")

            for row in reader:

                #print(row)

                # if len(row) != 12:
                #     continue  # o log
                # (
                #     cc, postal, place,
                #     admin1_name, admin1_code,
                #     admin2_name, admin2_code,
                #     admin3_name, admin3_code,
                #     lat, lon, acc
                # ) = row
                # # Sanity check
                # if len(cc) != 2 or not cc.isalpha():
                #     continue


                # Si prefieres forzar el ISO desde el nombre del zip:
                # cc = iso
                # insert_row(cc, postal, place, admin1_code, admin1_name,
                #            admin2_code, admin2_name, lat, lon, acc)
                
                # country code      : iso country code, 2 characters
                # postal code       : varchar(20)
                # place name        : varchar(180)
                # admin name1       : 1. order subdivision (state) varchar(100)
                # admin code1       : 1. order subdivision (state) varchar(20)
                # admin name2       : 2. order subdivision (county/province) varchar(100)
                # admin code2       : 2. order subdivision (county/province) varchar(20)
                # admin name3       : 3. order subdivision (community) varchar(100)
                # admin code3       : 3. order subdivision (community) varchar(20)
                # latitude          : estimated latitude (wgs84)
                # longitude         : estimated longitude (wgs84)
                # accuracy          : accuracy of lat/lng from 1=estimated, 4=geonameid, 6=centroid of addresses or shape

                if len(row) < 12:
                    continue  # o log

                print(iso)

                # Sanity check
                # if len(row[0]) != 2 or not row[0].isalpha():
                #     continue

                print(row)

                insert_row(iso, row[0], row[1], row[3], row[2],
                           row[5], row[4], row[8], row[9], row[10])
                
                #borrar
                break

def upsert_row(cur, row):
    (country, postal, place, a1, a1name, a2, a2name, a3, a3name, lat, lon, acc) = row
    cur.execute("""
        IF NOT EXISTS (
          SELECT 1 FROM dbo.POSTAL_CODES WITH (UPDLOCK, HOLDLOCK)
          WHERE COUNTRY_CODE=? AND POSTAL_CODE=? AND ISNULL(PLACE_NAME,'')=ISNULL(?, '')
        )
        INSERT INTO dbo.POSTAL_CODES (COUNTRY_CODE, POSTAL_CODE, PLACE_NAME, ADMIN1_CODE, ADMIN1_NAME, ADMIN2_CODE, ADMIN2_NAME, LATITUDE, LONGITUDE, ACCURACY)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ELSE
        UPDATE dbo.POSTAL_CODES
        SET ADMIN1_CODE=?, ADMIN1_NAME=?, ADMIN2_CODE=?, ADMIN2_NAME=?, LATITUDE=?, LONGITUDE=?, ACCURACY=?
        WHERE COUNTRY_CODE=? AND POSTAL_CODE=? AND ISNULL(PLACE_NAME,'')=ISNULL(?, '')
    """,
    country, postal, place,
    country, postal, place, a1, a1name, a2, a2name,
    float(lat) if lat else None, float(lon) if lon else None, int(acc) if acc else None,
    a1, a1name, a2, a2name, float(lat) if lat else None, float(lon) if lon else None, int(acc) if acc else None,
    country, postal, place)

# with pyodbc.connect(CONN_STR, autocommit=False) as conn:
#     cur = conn.cursor()
#     for fname in FILES:
#         with zipfile.ZipFile(fname) as zf:
#             print(f"Procesando {fname}...")
#             tsv_name = [n for n in zf.namelist() if n.lower().endswith(".txt") or n.lower().endswith(".csv")][0]
#             print(f" Leyendo {tsv_name}...")
#             with zf.open(tsv_name) as fh:
#                 text = io.TextIOWrapper(fh, encoding="utf-8")
#                 reader = csv.reader(text, delimiter='\t')
#                 for row in reader:
#                     if not row or len(row) < 12: continue
#                     upsert_row(cur, row[:12])
#         conn.commit()

# a) Carga un país (versión simple):
insert_row = make_insert_row(CONN_STR)
load_postal_zip(r"ES.zip", insert_row)

# # b) Carga varios países en batch (rápido):
# bi = BatchInserter(CONN_STR)
# for zip_path in [
#     r"C:\data\geonames\ES.zip",
#     r"C:\data\geonames\US.zip",
#     r"C:\data\geonames\PT.zip",
#     r"C:\data\geonames\MX.zip",
#     r"C:\data\geonames\VE.zip",
# ]:
#     load_postal_zip(zip_path, bi.insert_row)
# bi.close()
