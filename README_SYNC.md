# 🚀 Lisnave Gas Tracker - Sincronização em Tempo Real

## 📋 Descrição

Sistema completo de sincronização automática em tempo real para o Lisnave Gas Tracker. Permite que múltiplos usuários em diferentes dispositivos (PC, telemóvel, tablet) vejam as atualizações instantaneamente.

## 🏗️ Arquitetura

- **Backend**: Node.js + Express + Socket.IO
- **Database**: SQLite (simplicidade e portabilidade)
- **Frontend**: HTML5 + WebSocket
- **Sincronização**: Tempo real via WebSocket

## 🚀 Instalação e Configuração

### 1. Instalar Dependências do Servidor

```bash
cd c:\Users\andre.bras\Desktop\ant
npm install
```

### 2. Iniciar o Servidor

```bash
npm start
```

O servidor vai iniciar em: `http://localhost:3000`

### 3. Acessar a Aplicação Sincronizada

Abra no browser: `http://localhost:3000/index_sync.html`

## 🔄 Como Funciona

### Backend (server.js)
- **API REST** para operações CRUD
- **WebSocket** para sincronização em tempo real
- **SQLite** para persistência de dados
- **CORS** habilitado para multi-dispositivo

### Frontend (index_sync.html)
- **Socket.IO client** para conexão WebSocket
- **API calls** para salvar/editar dados
- **Atualização automática** quando outros usuários fazem mudanças
- **Status de conexão** visível no topo

## 📱 Funcionalidades

### ✅ Sincronização em Tempo Real
- **Adicionar garrafa**: Aparece instantaneamente em todos os dispositivos
- **Editar garrafa**: Atualizações visíveis em tempo real
- **Remover garrafa**: Desaparece de todas as telas
- **Mudar status**: Sincronizado automaticamente

### ✅ Multi-Dispositivo
- **PC**: Acesso completo com todas as funcionalidades
- **Telemóvel**: Interface otimizada com FAB buttons
- **Tablet**: Layout responsivo
- **Conexão simultânea**: Vários usuários ao mesmo tempo

### ✅ Indicadores Visuais
- **🔄 Conectado**: Status verde quando online
- **❌ Desconectado**: Status vermelho quando offline
- **🔄 Dados sincronizados**: Notificação quando há atualizações

## 🌐 Acesso de Rede

### Local (Mesma WiFi)
- PC: `http://localhost:3000/index_sync.html`
- Telemóvel: `http://[IP-DO-PC]:3000/index_sync.html`
  - Substitua `[IP-DO-PC]` pelo IP local (ex: 192.168.1.100)

### Para encontrar seu IP:
```bash
ipconfig
# Procure por "IPv4 Address" ou "Endereço IPv4"
```

## 📊 Estrutura de Dados

### Cilinders (Garrafas)
```json
{
  "id": "GAS-001",
  "type": "Acetileno",
  "zoneId": "DS1",
  "lat": 38.479,
  "lng": -8.792,
  "status": "ativa",
  "ts": "01/01/2025",
  "worker": "J. Ferreira",
  "pres": 145
}
```

### Workers (Operadores)
```json
["J. Ferreira", "M. Santos", "R. Costa", ...]
```

## 🔧 Configuração Avançada

### Porta do Servidor
Edite `server.js` para mudar a porta:
```javascript
const PORT = process.env.PORT || 8080; // Mude para 8080
```

### Database
O arquivo `lisnave_data.db` é criado automaticamente na primeira execução.

### CORS
Para produção, restrinja os origins em `server.js`:
```javascript
cors({
  origin: ["http://localhost:3000", "http://192.168.1.100:3000"]
})
```

## 🚨 Troubleshooting

### Problemas Comuns

#### 1. "Cannot GET /index_sync.html"
- **Causa**: Servidor não iniciado
- **Solução**: Execute `npm start`

#### 2. "Conexão recusada"
- **Causa**: Firewall ou porta bloqueada
- **Solução**: Verifique firewall e use porta 3000

#### 3. "CORS policy error"
- **Causa**: Acessando de IP diferente
- **Solução**: Configure CORS corretamente no server.js

#### 4. "Dados não sincronizam"
- **Causa**: WebSocket desconectado
- **Solução**: Verifique status de conexão (ícone 🔄/❌)

### Logs do Servidor
O servidor mostra logs detalhados:
- Clientes conectados/desconectados
- Operações de API
- Erros de database

## 📈 Performance

### Capacidade
- **Conexões simultâneas**: ~100 clientes
- **Garrafas por segundo**: ~100 operações
- **Latência**: <100ms em rede local

### Backup
- **Auto-backup**: Database SQLite
- **Exportação**: Funcionalidade de exportar JSON
- **Importação**: Funcionalidade de importar dados

## 🔐 Segurança

### Para Produção
1. **HTTPS**: Configure SSL/TLS
2. **Authentication**: Adicione login/senha
3. **Rate Limiting**: Limite requisições por IP
4. **Validation**: Valide todos os inputs
5. **Database Security**: Use PostgreSQL em produção

## 🚀 Deploy em Produção

### Opções Gratuitas
- **Heroku**: Node.js + PostgreSQL
- **Railway**: Container Docker
- **Render**: Backend as a Service

### Passos para Deploy
1. Configure variáveis de ambiente
2. Use PostgreSQL em vez de SQLite
3. Adicione autenticação
4. Configure HTTPS
5. Teste em ambiente de staging

## 📞 Suporte

### Debug
- **Console do browser**: F12 → Network/Console
- **Logs do servidor**: Terminal onde executou `npm start`
- **Status WebSocket**: Ícone 🔄/❌ no topo da página

### Teste de Conectividade
1. Abra a aplicação em 2 browsers diferentes
2. Adicione uma garrafa em um browser
3. Deve aparecer instantaneamente no outro

---

**🎯 Pronto! Agora você tem sincronização em tempo real completa entre todos os dispositivos!**
