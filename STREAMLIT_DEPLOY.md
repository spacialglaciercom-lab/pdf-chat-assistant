# Deploy to Streamlit Cloud

This guide will help you deploy your PDF Chat Assistant to Streamlit Cloud.

## Prerequisites

✅ Your code is already on GitHub at: https://github.com/spacialglaciercom-lab/pdf-chat-assistant.git

## Step-by-Step Deployment

### Step 1: Go to Streamlit Cloud

1. Visit https://share.streamlit.io/
2. Sign in with your **GitHub account** (use the same account that has access to the repository)
3. Click **"New app"** button

### Step 2: Connect Your Repository

1. **Repository**: Select `spacialglaciercom-lab/pdf-chat-assistant`
2. **Branch**: Select `main` (or `master` if that's your default branch)
3. **Main file path**: Enter `app.py`
4. Click **"Deploy!"**

### Step 3: Configure App Secrets (IMPORTANT!)

**You must add your OpenAI API key as a secret:**

1. After the app starts deploying, click on the **⚙️ (Settings)** icon (three dots menu → Settings)
2. Go to the **"Secrets"** tab
3. Click **"Edit secrets"** or **"New secret"**
4. Add your OpenAI API key in this format:

```toml
OPENAI_API_KEY = "your-openai-api-key-here"
```

**Important**: Replace `your-openai-api-key-here` with your actual OpenAI API key (remove the quotes in the actual secret entry)

5. Click **"Save"**

### Step 4: Wait for Deployment

- Streamlit Cloud will automatically install dependencies from `requirements.txt`
- The deployment usually takes 1-2 minutes
- You'll see build logs in real-time
- Once complete, your app will be live!

### Step 5: Access Your App

Your app will be available at:
```
https://pdf-chat-assistant-[your-username].streamlit.app
```

You can also find the URL in your Streamlit Cloud dashboard.

## Configuration Details

### Main File
- **File**: `app.py`
- **Location**: Root of repository

### Requirements
All dependencies are listed in `requirements.txt`:
- streamlit
- langchain
- langchain-openai
- langchain-community
- chromadb
- pypdf
- openai
- python-dotenv
- tiktoken

### Environment Variables
The app uses `.env` file locally, but on Streamlit Cloud, use **Secrets** instead:
- `OPENAI_API_KEY` - Your OpenAI API key (add via Secrets tab)

## Troubleshooting

### Build Failures

**Issue**: Build fails with dependency errors
- **Solution**: Check that all dependencies in `requirements.txt` are compatible
- Ensure Python version compatibility (app uses Python 3.11)

**Issue**: Import errors
- **Solution**: Verify all imports in `app.py` match the packages in `requirements.txt`

### Runtime Errors

**Issue**: "OPENAI_API_KEY not found" error
- **Solution**: Make sure you added the secret in Streamlit Cloud settings → Secrets
- Check that the secret name is exactly `OPENAI_API_KEY` (case-sensitive)

**Issue**: ChromaDB errors
- **Solution**: ChromaDB data is stored temporarily. For persistence, you may need to use external storage (this is a limitation of Streamlit Cloud's ephemeral filesystem)

### App Not Loading

**Issue**: App shows error page
- **Solution**: Check the logs in Streamlit Cloud dashboard
- Verify the main file path is correct (`app.py`)

## Updating Your App

After making changes to your code:

1. Commit and push changes to GitHub:
   ```bash
   git add .
   git commit -m "Your update message"
   git push
   ```

2. Streamlit Cloud will **automatically redeploy** your app (usually within 30 seconds)

## Best Practices

1. **Never commit API keys**: Your `.gitignore` already protects `.env` files
2. **Use Secrets**: Always use Streamlit Cloud Secrets for sensitive data
3. **Test locally first**: Test changes locally before pushing to GitHub
4. **Monitor usage**: Keep an eye on OpenAI API usage to avoid unexpected costs

## Cost Considerations

- **Streamlit Cloud**: Free for public repos
- **OpenAI API**: Pay-per-use (check OpenAI pricing)
- Consider setting usage limits in your OpenAI account

## Need Help?

- Streamlit Cloud Docs: https://docs.streamlit.io/streamlit-community-cloud
- Streamlit Community: https://discuss.streamlit.io/
- Check app logs in Streamlit Cloud dashboard for detailed error messages

