import gradio as gr
from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from langchain.prompts import ChatPromptTemplate

# Metadata mô tả bảng
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
    model="Qwen1.5-1.8B-Chat",
    openai_api_base=(
        "http://llm:8000/v1"  # Nếu chạy docker-compose
    ),
    openai_api_key="sk-xxx"
)

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}")
])

# Tạo agent
agent = create_sql_agent(
    llm=llm,
    db=db,
    verbose=True,
    system_message=SystemMessage(content=system_prompt)
)


def chatbot(query):
    try:
        result = agent.run(query)
        return result
    except Exception as e:
        return f"Lỗi: {str(e)}"


demo = gr.Interface(
    fn=chatbot,
    inputs=gr.Textbox(lines=2, label="Nhập câu hỏi"),
    outputs=gr.Textbox(lines=5, label="Trả lời"),
    title="Chatbot",
    description="Nhập câu hỏi về dữ liệu nhân sự, phòng ban, vai trò..."
)


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)