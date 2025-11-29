"""
ANALYTICS CONNECTION - Analiz Veritabanı Bağlantısı (sr_analiz_db)
"""

import os
import psycopg2
import logging
from dotenv import load_dotenv


class AnalyticsConnection:
    """
    Analiz veritabanı (sr_analiz_db) - Tahmin sistemi için
    """
    
    def __init__(self, env_file='.env.analytics'):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Analiz veritabanı konfigürasyonunu yükle
        env_path = os.path.join(os.path.dirname(__file__), env_file)
        load_dotenv(env_path)
        
        self.host = os.getenv('ANALİZ_DB_HOST')
        self.port = int(os.getenv('ANALİZ_DB_PORT', '5432'))
        self.database = os.getenv('ANALİZ_DB_NAME')
        self.user = os.getenv('ANALİZ_DB_USER')
        self.password = os.getenv('ANALİZ_DB_PASSWORD')
        self.database_url = os.getenv('ANALİZ_DATABASE_URL')
        
        print(f"🔌 ANALYTICS DB: {self.database} @ {self.host}")
        
        # Validation
        if not all([self.host, self.database, self.user, self.password]):
            raise ValueError("❌ ANALYTICS DB: Gerekli environment değişkenleri eksik!")
    
    def connect(self):
        """Analiz veritabanına bağlan"""
        try:
            conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password
            )
            return conn
        except Exception as e:
            self.logger.error(f"❌ Analiz DB bağlantı hatası: {e}")
            return None
    

    def query(self, sql, params=None):
        """Basit query fonksiyonu - Tuple listesi döndürür"""
        conn = self.connect()
        if not conn:
            return None
        
        cursor = conn.cursor()
        cursor.execute(sql, params)
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data
    
    def execute_query(self, sql, params=None):
        """Execute fonksiyonu - INSERT/UPDATE/DELETE/CREATE için"""
        conn = self.connect()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            self.logger.error(f"❌ Execute query hatası: {e}")
            conn.rollback()
            conn.close()
            return False
    
    def query_df(self, sql, params=None):
        """Pandas DataFrame döndüren query fonksiyonu"""
        import pandas as pd
        
        conn = self.connect()
        if not conn:
            return None
            
        try:
            df = pd.read_sql_query(sql, conn, params=params)
            conn.close()
            return df
        except Exception as e:
            self.logger.error(f"❌ DataFrame query hatası: {e}")
            conn.close()
            return None
    
    def bulk_df(self, df, table_name, replace=True):
        """
        DataFrame'i analiz veritabanına yükle
        
        Args:
            df: Pandas DataFrame
            table_name: Hedef tablo adı
            replace: True = tablo varsa sil ve yeniden oluştur, False = append
        """
        import pandas as pd
        import io
        
        conn = self.connect()
        if not conn:
            return False
            
        try:
            cursor = conn.cursor()
            
            # Tablo var mı kontrol et
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = %s
                )
            """, (table_name,))
            
            result = cursor.fetchone()
            table_exists = result[0] if result else False
            
            if table_exists and replace:
                print(f"🗑️ {table_name} tablosu siliniyor...")
                cursor.execute(f"DROP TABLE {table_name}")
                conn.commit()
                table_exists = False
            
            if not table_exists:
                # Tablo oluştur
                print(f"🔨 {table_name} tablosu oluşturuluyor...")
                
                # Sütun tiplerini belirle
                columns = []
                for col in df.columns:
                    # Zaman damgası alanları için özel tip
                    if col in ['created_at', 'updated_at']:
                        columns.append(f'"{col}" TIMESTAMP')
                    elif df[col].dtype == 'object':
                        columns.append(f'"{col}" TEXT')
                    elif df[col].dtype in ['int64', 'int32']:
                        columns.append(f'"{col}" INTEGER')
                    elif df[col].dtype in ['float64', 'float32']:
                        columns.append(f'"{col}" FLOAT')
                    else:
                        columns.append(f'"{col}" TEXT')
                
                create_sql = f"CREATE TABLE {table_name} ({', '.join(columns)})"
                cursor.execute(create_sql)
                conn.commit()
            
            # Veri yükle
            print(f"⚡ {len(df):,} kayıt {table_name} tablosuna yükleniyor...")
            
            output = io.StringIO()
            df.to_csv(output, sep='\t', header=False, index=False, na_rep='\\N')
            output.seek(0)
            
            columns = ','.join([f'"{col}"' for col in df.columns])
            copy_sql = f"COPY {table_name} ({columns}) FROM STDIN WITH CSV DELIMITER E'\\t' NULL '\\N'"
            cursor.copy_expert(copy_sql, output)
            
            conn.commit()
            cursor.close()
            conn.close()
            
            action = "oluşturuldu" if not table_exists or replace else "genişletildi"
            print(f"✅ {table_name} tablosu {action} ({len(df):,} kayıt)")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Bulk DataFrame hatası: {e}")
            conn.rollback()
            conn.close()
            return False