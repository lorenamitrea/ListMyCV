import re
import os
from flask import Flask, request, render_template, jsonify, redirect


app = Flask(__name__)
app.config.from_object(__name__)


if __name__ == "__main__":
    app.run()
