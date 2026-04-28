# 📱 Como Instalar a App Lisnave no Telemóvel

## 🌐 Opção 1: Hospedagem Online (Recomendado)

### Serviços Gratuitos:
1. **GitHub Pages** (mais fácil)
2. **Netlify** 
3. **Vercel**
4. **Firebase Hosting**

### Usando GitHub Pages:

#### 1. Criar Conta no GitHub
- Aceda a https://github.com
- Crie uma conta gratuita

#### 2. Criar Novo Repositório
- Click em "New repository"
- Nome: `lisnave-gas-tracker`
- Público
- Não adicione README

#### 3. Upload dos Ficheiros
- Click em "Add file" → "Upload files"
- Arraste todos os ficheiros da pasta `ant`:
  - `index.html`
  - `manifest.json`
  - `sw.js`
  - `icon-192.png`
  - `icon-512.png`
  - `Logotipo_Lisnave.png`
  - `lisnave_sat_offline.png`

#### 4. Ativar GitHub Pages
- Vá para "Settings" → "Pages"
- Source: "Deploy from a branch"
- Branch: "main"
- Folder: "/ (root)"
- Click "Save"

#### 5. Aguardar Deploy
- Espere 2-5 minutos
- Aceda ao URL: `https://[seu-username].github.io/lisnave-gas-tracker`

---

## 📲 Instalar no Telemóvel

### Android:
1. Abra o URL no Chrome
2. Espere carregar completamente
3. Click no menu (3 pontos) → "Instalar aplicação" ou "Adicionar ao ecrã inicial"
4. Confirme a instalação
5. A app aparecerá no ecrã principal

### iOS:
1. Abra o URL no Safari
2. Espere carregar completamente  
3. Click no ícone de partilha (quadrado com seta)
4. Scroll para baixo → "Adicionar ao ecrã inicial"
5. Confirme "Adicionar"

---

## 🔄 Opção 2: Servidor Local (Apenas na mesma rede)

### Para Testes Rápidos:

#### 1. Obter IP do Computador
```cmd
ipconfig
```
- Procure "IPv4 Address" (ex: 192.168.1.100)

#### 2. Iniciar Servidor com IP Específico
```cmd
cd c:\Users\andre.bras\Desktop\ant
python -m http.server 8080 --bind 0.0.0.0
```

#### 3. Aceder do Telemóvel
- Conecte o telemóvel à mesma WiFi
- Abra o browser: `http://192.168.1.100:8080`
- Siga os passos de instalação acima

---

## ⚠️ Importante

### Requisitos PWA:
- **HTTPS obrigatório** (exceto localhost/IP local)
- **Conexão internet** na primeira instalação
- **Funciona offline** depois de instalada

### Permissões Necessárias:
- **GPS** para localização (opcional)
- **Storage** para dados offline
- **Notificações** (se implementar)

---

## 🚀 Teste Rápido

### URL de Teste:
Se usar GitHub Pages: `https://[seu-username].github.io/lisnave-gas-tracker`

### Verificar Funcionalidades:
- ✅ Mapa carrega
- ✅ Garrafas aparecem
- ✅ FAB buttons funcionam
- ✅ Modo offline funciona
- ✅ Instalação PWA disponível

---

## 🔧 Problemas Comuns

### "Instalar App" não aparece:
- Verifique se está usando HTTPS
- Verifique se todos os ficheiros estão online
- Tente recarregar a página

### Mapa não carrega:
- Verifique conexão internet
- Limpe cache do browser
- Verifique console para erros

### Dados não salvam:
- Verifique se localStorage está ativado
- Tente reinstalar a app

---

## 📁 Ficheiros Essenciais

Não se esqueça de incluir:
- ✅ `index.html` (principal)
- ✅ `manifest.json` (PWA config)
- ✅ `sw.js` (service worker)
- ✅ `icon-192.png` e `icon-512.png` (ícones)
- ✅ `Logotipo_Lisnave.png` (logo)
- ✅ `lisnave_sat_offline.png` (mapa offline)
