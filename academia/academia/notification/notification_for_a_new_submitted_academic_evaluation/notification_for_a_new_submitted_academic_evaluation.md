<h3>{{_("Academic Evaluation")}}</h3>

<p>{{_("Dear ") }} {{ doc.evaluatee_party_name}} {{_(", a new submitted academic evaluation associated with you: ") }} {{ doc.name }}</p>

<b>Evaluation Summary</b><br>

<b>{{_("Evaluator Name: ") }}</b> {{ doc.evaluator_party_name }}<br>

<b>{{_("Evaluation Template Type: ") }}</b> {{ doc.template }}<br><br>

<table border=1 >
    <tr align="center">
        <th>Criterion</th>
        <th>Evaluation</th>
    </tr>
    {% for eval in doc.evaluation_details %}
        <tr align="center">
            <td> {{ eval.criterion }} </td>
            <td> {{ eval.evaluation }} </td>
        </tr>
    {% endfor %}
</table>