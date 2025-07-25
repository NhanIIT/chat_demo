from flask import Flask, request, jsonify
from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage

# Metadata mô tả bảng
# PEP8: break long lines

table_metadata = {
    "users": (
        "Bảng lưu thông tin nhân sự: id, name (tên), department_id "
        "(phòng ban), "
        "email, "
        "role_id (vai trò)"
    ),
    "departments": (
        "Bảng phòng ban: id, name (tên phòng ban)"
    ),
    "roles": (
        "Bảng vai trò: id, name (tên vai trò)"
    ),
    "permissions": (
        "Bảng quyền: id, name (tên quyền)"
    ),
    "user_roles": (
        "Liên kết user với role: user_id, role_id"
    )
}

system_prompt = (
    "Bạn là trợ lý AI, có thể sinh truy vấn SQL dựa trên yêu cầu người dùng. "
    "Dưới đây là mô tả các bảng:\n"
    + "\n".join([
        f"{k}: {v}" for k, v in table_metadata.items()
    ])
)

# Kết nối database
db = SQLDatabase.from_uri("sqlite:///hr.db")

# Kết nối LLM Qwen qua OpenAI API (vLLM)
llm = ChatOpenAI(
    model="Qwen3-1.7B",
    openai_api_base="http://llm:8000/v1",
    openai_api_key="sk-xxx"
)


# Tạo agent
agent = create_sql_agent(
    llm=llm,
    db=db,
    verbose=True,
    system_message=SystemMessage(content=system_prompt)
)

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return "Chatbot"


@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_query = data.get("query", "")
    try:
        result = agent.run(user_query)
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)