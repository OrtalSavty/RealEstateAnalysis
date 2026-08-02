# עבודה עם טבלאות נתונים 
import pandas as pd
import numpy as np
# איתור וקריאת קבצים מרובים מתיקיות המחשב
import glob 
import os


# נתיב אל הקבצים של הנתונים
path = "../data/raw"
#מאתר את כל הקבצים עם סיומת csv
# הכוכבית מסמנת שנראה את כל הקבצים עם הסיומת הבאה בתוך הנתיב ששמנו
# רשימה של כל הכתובות של הקבצי נתונים שלנו
all_files = glob.glob(os.path.join(path,"*.csv"))

# ניייצר רשימה ריקה שבתוכה נשמור את כל הטבלאות לפני שנאחד אותם
df_list = []

# מעבר על כל הנתיבים
for file in all_files:
    # נחריז שהקוד הבא עלול לזרוק שגיע אם פייתון לא תצליח לקרוא את הנתונים בצורה תקינה    
    try:
        # קריאה של הקובץ מהנתיב הנוכחי והגדרה שהקובץ לא יתפקשש גם אם הוא בעברית        
        # נשמור את הקובץ שקראנו במשתנה עזר זמני        
        # file, encoding_errors='ignore' אומר לפייתון להתעלם מתווים בעיתיים
        # encoding='utf-8' אומר לפייתון שהקובץ יכיל נתונים בעברית אז שלא יבלגן אותם
        df = pd.read_csv(file, encoding_errors='ignore', encoding='utf-8')
        # הוספה של הקובץ למשתנה הטבלאות שלנו        
        df_list.append(df)
        
    # אם יש שגיאה והקובץ נפל תזרוק שגיאה ותמשיך אל תיפול    
    except Exception as e:
        print(f"could not read {file}: {e}")

# חיבור של כל הטבלאות ששמרנו לטבלת נתונים אחת גדולה
# ignore_index=True הגדרנו שיתעלם מהאינדקסים בטבלה ויעשה אינדקסים חדשים שהטבלה תיהיה מסודרת
all_data = pd.concat(df_list, ignore_index=True)

# נסגר את השמות לאנגלית
# מתן שמות חדשים ונקיים באנגלית לעמודות
all_data.columns = ['id','address','area','date', 'price','Block and parcel','neighborhood','rooms','floor', 'A trend of change']

# ניקוי עמודת המחיר
# הסרת סימני מטבע (₪), פסיקים או רווחים והמרה למספר
# astype המרה למחרוזת
# replace החלפה של הסימנים שלא נרצה כמו מטבע ופסיקים לרווחים
# .str.strip() הסרה של הרווחים המיותרים  
# pd.to_numeric המרה למספר
all_data['price'] = all_data['price'].astype(str).str.replace('₪', '', regex=True)
all_data['price'] = all_data['price'].str.replace(',', '', regex=True).str.strip()
all_data['price'] = pd.to_numeric(all_data['price'], errors='coerce')

# מחיקה של העמודת כתובת
all_data = all_data.drop(columns= 'address')

# שמירה של המילים שנרצה להחליף מהנתונים
missing_values_list = ["לא ידוע", "ללא תיכנון", "לא ידוע ", "nan", "NaN"]
# החלפה של כל הנתונים "לא ידוע" לnan
all_data.replace(missing_values_list, np.nan, inplace=True)

# בדיקה כמה שורות ועמודות יש לנו בטבלת הנתונים הגדולה
print("shape:", all_data.shape)
print("")

# הוצאה של ה5 שורות הראשונות מהטבלה כדי להבין איך היא נראת
print(all_data.head())
# נבדוק כמה ערכים ריקים יש בטבלה
isnull = all_data.isnull()
# נדפיס כמה סה"כ ערכים חסרים יש
print("\nThe number of missing values ​​is:\n" ,isnull.sum())
# נדפיס סיכום סטטיסטי של הנתונים
statistical = all_data.describe()





