from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
x,y=make_classification(
    n_samples=1000,
    n_features=15,
    random_state=42
)
x_train, x_test, y_train,y_test=train_test_split(
    x,y,
    test_size=0.2,
    random_state=42
)
scaler=StandardScaler()
x_train_scaled=scaler.fit_transform(x_train)

x_test_scaled=scaler.transform(x_test)
model=RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(x_train_scaled, y_train)

y_pred=model.predict(x_test_scaled)
acc=accuracy_score(y_test, y_pred)
print(f'Dokładność klasyfikacji: {acc:.2%}')
print()
print('Raport Klasyfikacji')
print(classification_report(y_test, y_pred))