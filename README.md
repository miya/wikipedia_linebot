# wikipedia_linebot

## debug
#### ngrokのインストール
```
$ brew install cask ngrok
```

#### ngrokの起動(8000番ポートを開放)
```
$ ngrok http 8000
```

#### flaskのポート番号をngrokで開けた番号と同じにする 
```python
app.run(host="0.0.0.0", port=8000, threaded=True, debug=True)
```

#### 実行 
```
$ python3 main.py 
```





