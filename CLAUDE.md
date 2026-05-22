# Schoology Help Frontend

A web-based dashboard for PAUSD Schoology.

## Files

- `index.html` - Frontend web interface (single-page app)

## Setup

Simply open `index.html` in a browser, or serve it with any static file server.

## Architecture

The frontend communicates with the external API server at `jchat.fly.dev/schoology` via REST API.

This is a client-only application - the server-side code is at https://github.com/indiamonda/chat/