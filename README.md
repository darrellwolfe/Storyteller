# Storyteller

This repository has been scaffolded with a minimal static blog structure you can publish on GitHub Pages.

Files added:

- `docs/index.html` — home page of the blog.
- `docs/posts/2025-10-26-welcome.html` — sample post.
- `docs/assets/css/style.css` — basic styling.

How to publish on GitHub Pages

1. In your repository on GitHub, go to Settings → Pages.
2. Under "Source", select Branch: `main` and folder: `/docs` and save.
3. GitHub will publish the site; the page URL will be shown on the same settings page.

Preview locally

You can preview the `docs/` folder locally using a simple HTTP server (from repository root):

```bash
# Python 3
python3 -m http.server --directory docs 8000

# then open http://localhost:8000 in your browser
```

Next steps

- Add new posts as HTML files under `docs/posts/` and add links to them from `docs/index.html`.
- If you'd like the site converted to a Jekyll or Hugo setup (with templating, collections, and convenience for writing posts in Markdown), tell me which generator you prefer and I can convert it.

If you'd like a GitHub Actions workflow to build and deploy (for example, compile a static site generator), I can add that too.

Automatically generating the index

To make adding posts easier you can run a small generator that scans `docs/posts/` and updates the posts list in `docs/index.html`.

Usage:

```bash
# from repository root
python3 scripts/generate_index.py
```

The generator looks for these markers in `docs/index.html` and replaces the content between them:

<!-- POSTS_START -->
<!-- POSTS_END -->

After running the generator you can preview the site locally as before:

```bash
python3 -m http.server --directory docs 8000
# then open http://localhost:8000
```

Jekyll / GitHub Pages

I've added a Jekyll scaffold under `docs/` including `_config.yml`, `_layouts/`, and an example post in `_posts/`. You can build the site locally with Bundler:

```bash
# install ruby gems (requires Ruby)
gem install bundler
bundle install

# build the site from the docs/ source into ./public
bundle exec jekyll build --source docs --destination public

# preview the generated files
python3 -m http.server --directory public 8000
```

GitHub Actions will build the site on push to `main` and deploy it to Pages using the `actions/deploy-pages` action. Ensure Pages is configured to use the repository's build-in Pages (the action will manage deployment). If you'd like the site to use a custom domain or other settings, tell me and I'll update the workflow and config.
Darrell Wolfe, Storyteller. A personal blog. 
