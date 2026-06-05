# Deployment Guide for Secure Folder Command Center

## Prerequisites

- Docker & Docker Compose installed
- Server with at least 2GB RAM
- Domain name (gatewaynexus.org)
- SSL certificate (Let's Encrypt - free)

## Quick Start Deployment

### 1. Clone Repository
```bash
git clone https://github.com/850011000kylebrucedowning/Ai-framework.git
cd Ai-framework/secure_center
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env with your API keys and credentials
nano .env
```

### 3. Run Deployment Script
```bash
chmod +x deploy.sh
./deploy.sh
```

The script will:
- ✅ Check Docker installation
- ✅ Create necessary directories
- ✅ Generate self-signed SSL certificate
- ✅ Build Docker images
- ✅ Start all services
- ✅ Verify health status

### 4. Access Application
- **Web Interface**: https://your-domain.com
- **API**: https://your-domain.com/api
- **Default Port**: 443 (HTTPS), 80 (HTTP redirect)

---

## Manual Deployment Steps

If you prefer manual control:

### Step 1: Install Docker & Docker Compose
```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### Step 2: Start Services
```bash
docker-compose up -d
```

### Step 3: Verify Status
```bash
docker-compose ps
docker-compose logs -f
```

---

## Production Setup with Let's Encrypt

### 1. Install Certbot
```bash
sudo apt-get update
sudo apt-get install certbot python3-certbot-nginx
```

### 2. Generate Certificate
```bash
sudo certbot certonly --standalone -d gatewaynexus.org -d www.gatewaynexus.org
```

### 3. Update Nginx Config
Replace certificate paths in `nginx.conf`:
```
ssl_certificate /etc/letsencrypt/live/gatewaynexus.org/fullchain.pem;
ssl_certificate_key /etc/letsencrypt/live/gatewaynexus.org/privkey.pem;
```

### 4. Auto-Renewal
```bash
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer
```

---

## DNS Configuration

Point your domain to the server:

1. **A Record**: 
   - Name: @
   - Value: YOUR_SERVER_IP
   - TTL: 3600

2. **CNAME Record** (for www):
   - Name: www
   - Value: gatewaynexus.org
   - TTL: 3600

---

## Docker Commands Reference

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f api
docker-compose logs -f nginx

# Restart service
docker-compose restart api

# Rebuild images
docker-compose build --no-cache

# Execute command in container
docker-compose exec api bash

# Remove all containers (destructive)
docker-compose down -v
```

---

## Environment Variables

### Required
- `COMPLIANCE_SIGNING_KEY` - Min 32 characters for audit signatures
- `SMTP_SERVER` - Email server (e.g., smtp.gmail.com)
- `EMAIL_USER` - Email address
- `EMAIL_PASSWORD` - Email password or app password
- `STRIPE_API_KEY` - Stripe API key (optional)

### Optional
- `IMAP_SERVER` - For email receiving
- `ENCRYPTION_KEY` - For file encryption
- `DB_USER` - Database username
- `DB_PASSWORD` - Database password

---

## Monitoring & Maintenance

### Check Service Health
```bash
curl https://gatewaynexus.org/health
```

### View Real-time Logs
```bash
docker-compose logs -f --tail=100
```

### Database Backup
```bash
docker-compose exec postgres pg_dump -U secure_user secure_center_db > backup.sql
```

### Database Restore
```bash
cat backup.sql | docker-compose exec -T postgres psql -U secure_user secure_center_db
```

---

## Scaling

### Increase API Workers
Edit `Dockerfile`:
```dockerfile
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "8", "--timeout", "120", "api_server:app"]
```

### Enable Database
Edit `docker-compose.yml`:
```bash
docker-compose --profile production up -d
```

---

## Security Checklist

- [ ] Update all credentials in `.env`
- [ ] Install real SSL certificate (Let's Encrypt)
- [ ] Configure strong database passwords
- [ ] Enable firewall (ufw, iptables)
- [ ] Set up log rotation
- [ ] Regular backups enabled
- [ ] HTTPS redirect enabled
- [ ] Security headers configured
- [ ] Rate limiting enabled
- [ ] Regular security audits

---

## Troubleshooting

### API not responding
```bash
docker-compose logs api
docker-compose restart api
```

### SSL certificate issues
```bash
docker-compose logs nginx
# Check certificate paths in nginx.conf
```

### Database connection error
```bash
docker-compose logs postgres
# Verify DB credentials in .env
```

### Port already in use
```bash
# Find process on port 80/443
sudo lsof -i :80
sudo lsof -i :443
# Kill process or change port in docker-compose.yml
```

---

## Support & Updates

Monitor logs regularly:
```bash
docker-compose logs --tail=1000 -f
```

Update containers:
```bash
docker-compose pull
docker-compose up -d
```

---

## Deployment Checklist

Before going live:

- [ ] Domain configured and DNS propagated
- [ ] SSL certificate installed
- [ ] Environment variables configured
- [ ] Database backed up
- [ ] Application tested
- [ ] Logging enabled
- [ ] Monitoring configured
- [ ] Firewall rules set
- [ ] Backup strategy implemented
- [ ] Team trained on operations

---

**Need help?** Check logs with `docker-compose logs -f` or review individual service documentation.
