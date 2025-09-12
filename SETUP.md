# FinFriend Setup Guide

This guide explains how to configure FinFriend to use the free aitools-llm-proxy service for cost-free AI assistance.

## Quick Setup

1. **Get your credentials** from your instructor:
   - Username (e.g., `alice`)
   - 4-digit PIN (e.g., `1234`)

2. **Run the setup tool**:
   ```bash
   python finfriend-setup.py --username alice --pin 1234
   ```

3. **Start FinFriend**:
   ```bash
   streamlit run 🏠_FinFriend.py
   ```

That's it! FinFriend will now use the free `openai--gpt-oss-120b` model through aitools-llm-proxy.

## Setup Tool Options

### Basic Usage
```bash
python finfriend-setup.py --username <your_username> --pin <your_pin>
```

### Verify Token (Recommended)
```bash
python finfriend-setup.py --username alice --pin 1234 --verify
```
This tests the token before writing the configuration file.

### Custom Proxy URL
```bash
python finfriend-setup.py --username alice --pin 1234 --proxy-url http://different.server:8080
```

### Help
```bash
python finfriend-setup.py --help
```

## What the Setup Tool Does

1. **Registers** your username/PIN with aitools-llm-proxy
2. **Receives** a secure JWT token for API access
3. **Backs up** your existing `.env` file (if any)
4. **Creates** a new `.env` file with:
   - `OPENAI_API_BASE_URL=http://aitools.cs.vt.edu:7860/opensource/v1`
   - `OPENAI_API_KEY=<your_jwt_token>`
   - `OPENAI_API_MODEL=openai--gpt-oss-120b`

## Benefits

- **Free**: No cost for students to use the AI assistant
- **Powerful**: Uses the `openai--gpt-oss-120b` model (120 billion parameters)
- **Secure**: JWT-based authentication with your unique credentials
- **Simple**: One-time setup, then FinFriend works normally

## Troubleshooting

### Registration Failed
- **Check your username and PIN** with your instructor
- **Verify the PIN is exactly 4 digits**
- **Try again** - the service might be temporarily busy

### Token Verification Failed
- **Check your internet connection**
- **Verify the proxy server is accessible**: http://aitools.cs.vt.edu:7860
- **Contact your instructor** if problems persist

### FinFriend Won't Start
- **Make sure you ran the setup tool successfully**
- **Check the `.env` file exists** and has the correct format
- **Run setup again** if needed

## Advanced Usage

### Multiple Users
Each user needs their own username/PIN. Run setup separately:
```bash
python finfriend-setup.py --username alice --pin 1234    # Alice's setup
python finfriend-setup.py --username bob --pin 5678      # Bob's setup  
```

### Existing .env Files
The setup tool automatically backs up existing `.env` files with timestamps:
- `.env.backup.20250912_155530`

### Token Expiration
JWT tokens expire after 7 days. If FinFriend stops working:
1. Run the setup tool again with your same credentials
2. This will generate a fresh token

## Development

To add the setup tool to other projects:
1. Copy `finfriend-setup.py`
2. Add `httpx` to your dependencies
3. Modify the `.env` template in `write_env_file()` as needed

## Security Notes

- **Never share your JWT token** - it provides access to the AI service
- **Keep your username/PIN secure** - treat them like a password
- **Backup files are created locally** - they contain your previous tokens
- **JWT tokens expire** - re-run setup when needed (every ~7 days)
