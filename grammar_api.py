from flask import Flask, request, jsonify, render_template_string
import language_tool_python

app = Flask(__name__)
tool = language_tool_python.LanguageToolPublicAPI('en-US')

HTML_FORM = '''
<!DOCTYPE html>
<html>
<head>
    <title>Grammar Checker</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        textarea { width: 100%; height: 120px; }
        .result { margin-top: 20px; }
        .error { color: #b00; }
        .suggestion { color: #080; }
    </style>
</head>
<body>
    <h2>Grammar Checker</h2>
    <form id="grammarForm">
        <textarea id="text" name="text" placeholder="Paste your text here..."></textarea><br>
        <button type="submit">Check Grammar</button>
    </form>
    <div class="result" id="result"></div>
    <script>
    document.getElementById('grammarForm').onsubmit = async function(e) {
        e.preventDefault();
        const text = document.getElementById('text').value;
        document.getElementById('result').innerHTML = 'Checking...';
        const response = await fetch('/check', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text })
        });
        const data = await response.json();
        if (data.error) {
            document.getElementById('result').innerHTML = '<span class="error">' + data.error + '</span>';
        } else if (data.count === 0) {
            document.getElementById('result').innerHTML = '<span class="suggestion">No grammar issues found!</span>';
        } else {
            let html = `<b>Found ${data.count} issue(s):</b><ul>`;
            data.matches.forEach(function(match, i) {
                html += `<li><b>${i+1}.</b> ${match.message}<br>` +
                        `<span class='error'>Error:</span> '${match.error}'<br>` +
                        `<span class='suggestion'>Suggestion(s):</span> ${match.suggestions.length ? match.suggestions.join(', ') : 'None'}<br>` +
                        `<span>Context:</span> ...${match.context}...</li><br>`;
            });
            html += '</ul>';
            document.getElementById('result').innerHTML = html;
        }
    };
    </script>
</body>
</html>
'''

@app.route('/', methods=['GET'])
def home():
    return render_template_string(HTML_FORM)

@app.route('/check', methods=['POST'])
def check_grammar():
    data = request.get_json()
    text = data.get('text', '')
    if not text.strip():
        return jsonify({'error': 'No text provided.'}), 400
    matches = tool.check(text)
    results = []
    for match in matches:
        results.append({
            'message': match.message,
            'error': text[match.offset:match.offset + match.errorLength],
            'suggestions': match.replacements,
            'context': text[max(0, match.offset-20):match.offset+match.errorLength+20]
        })
    return jsonify({'matches': results, 'count': len(results)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5008) 