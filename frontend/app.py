import sys
from pathlib import Path
from uuid import uuid4

import streamlit as st
from langgraph.types import Command




# ============================================================
# Project path
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from domains.followup.graphs.process_reply_graph import build_process_reply_graph

# ============================================================
# Streamlit config
# ============================================================

st.set_page_config(
    page_title="Dental AI Follow-up",
    page_icon="🦷",
    layout="wide",
)


# ============================================================
# Graph
# ============================================================

@st.cache_resource
def get_graph():
    return build_process_reply_graph()


graph = get_graph()


# ============================================================
# Demo Data
# ============================================================

PATIENT_CONTEXT = {
    "patient_name": "王女士",
}

FOLLOWUP_ID = "F001"
PATIENT_ID = "P001"
TREATMENT_ID = "T001"

INITIAL_MESSAGE = (
    "王女士您好，想跟进一下您术后的恢复情况。"
    "请问现在疼痛、出血、肿胀或发热的情况怎么样？"
)

# ============================================================
# Helper
# ============================================================
def new_thread_id():
    return f"followup:{FOLLOWUP_ID}:{uuid4()}"



# ============================================================
# Session State
# ============================================================

if "thread_id" not in st.session_state:
    st.session_state.thread_id = new_thread_id()

if "followup_started" not in st.session_state:
    st.session_state.followup_started = False

if "waiting_for_patient" not in st.session_state:
    st.session_state.waiting_for_patient = False

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "clinic",
            "content": INITIAL_MESSAGE,
        }
    ]

if "latest_result" not in st.session_state:
    st.session_state.latest_result = None

if "draft_reply" not in st.session_state:
    st.session_state.draft_reply = ""

if "last_error" not in st.session_state:
    st.session_state.last_error = None


# ============================================================
# Helpers
# ============================================================

def reset_followup():
    st.session_state.thread_id = new_thread_id()
    st.session_state.followup_started = False
    st.session_state.waiting_for_patient = False

    st.session_state.messages = [
        {
            "role": "clinic",
            "content": INITIAL_MESSAGE,
        }
    ]

    st.session_state.latest_result = None
    st.session_state.draft_reply = ""
    st.session_state.last_error = None


def run_graph(patient_reply: str):
    config = {
        "configurable": {
            "thread_id": st.session_state.thread_id
        }
    }

    # ========================================================
    # First patient reply
    # ========================================================

    if not st.session_state.followup_started:

        initial_state = {
            "followup_id": FOLLOWUP_ID,
            "patient_id": PATIENT_ID,
            "treatment_id": TREATMENT_ID,
            "patient_context": PATIENT_CONTEXT,

            "patient_reply": patient_reply,
            "patient_reply_history": [patient_reply],
        }

        result = graph.invoke(
            initial_state,
            config=config,
        )

        st.session_state.followup_started = True

    # ========================================================
    # Resume after ASK_MORE interrupt
    # ========================================================

    elif st.session_state.waiting_for_patient:

        result = graph.invoke(
            Command(resume=patient_reply),
            config=config,
        )

    # ========================================================
    # Previous graph already completed
    # Start another execution for demo
    # ========================================================

    else:

        st.session_state.thread_id = new_thread_id()

        config = {
            "configurable": {
                "thread_id": st.session_state.thread_id
            }
        }

        initial_state = {
            "followup_id": FOLLOWUP_ID,
            "patient_id": PATIENT_ID,
            "treatment_id": TREATMENT_ID,
            "patient_context": PATIENT_CONTEXT,

            "patient_reply": patient_reply,
            "patient_reply_history": [patient_reply],
        }

        result = graph.invoke(
            initial_state,
            config=config,
        )

    st.session_state.latest_result = result

    st.session_state.waiting_for_patient = bool(
        result.get("__interrupt__")
    )

    st.session_state.draft_reply = (
        result.get("next_reply") or ""
    )


# ============================================================
# Header
# ============================================================

title_col, reset_col = st.columns([8, 1])

with title_col:
    st.title("🦷 Dental AI Follow-up Demo")

    st.caption(
        "患者回复 → AI 信息提取 → Policy 判断 → "
        "咨询师审核 → 发送给患者"
    )

with reset_col:
    st.write("")
    st.write("")

    if st.button(
        "Reset",
        use_container_width=True,
    ):
        reset_followup()
        st.rerun()


st.divider()

# ============================================================
# Demo Guide
# ============================================================

with st.expander("ℹ️ 这个 Demo 在测试什么？", expanded=False):

    guide_col, test_col = st.columns([1, 1], gap="large")

    # ========================================================
    # LEFT — Demo introduction
    # ========================================================

    with guide_col:

        st.markdown(
            """
这个 Demo 用来验证一条完整的术后回访流程：

**患者回复 → AI 提取关键信息 → Policy 判断 → AI 生成建议回复 → 咨询师审核后发送**

#### 当前重点测试

- AI 能不能正确提取疼痛、出血、肿胀、发热等信息
- 信息不完整时，能不能继续追问
- 出现高风险情况时，能不能升级给医生
- 咨询师是否可以审核、修改，再发送回复

#### 当前边界

- POC Demo，不连接真实 HIS 和企业微信
- 不做医疗诊断
- 不自动提供治疗或用药建议
- 患者、治疗和回访数据均为模拟数据
"""
        )

    # ========================================================
    # RIGHT — Test cases
    # ========================================================

    with test_col:

        st.markdown("### 🧪 Try it yourself")
        st.caption("复制下面任意一句到「患者端」进行测试。")

        st.markdown("#### 1. NORMAL")

        st.code(
            "现在疼痛3分，没有出血，有一点肿，没有发烧。",
            language=None,
        )

        st.markdown(
            """
**Expected Result:** `NORMAL` - 信息完整，未命中高风险规则 → 生成正常回访建议。
"""
        )

        st.markdown("#### 2. ASK_MORE")

        st.code(
            "现在没有出血，也没有发烧。",
            language=None,
        )

        st.markdown(
            """
**Expected Result:** `ASK_MORE` - 缺少疼痛和肿胀信息 → AI 继续向患者追问。
"""
        )
        st.caption("收到 AI 追问后，继续复制下面这句话回复：")
        st.code(
            "疼痛大概3分，有一点肿。",
            language=None,
        )

        st.markdown("#### 3. ESCALATE")
        st.code(
            "现在疼痛8分，而且还在出血，没有发烧。",
            language=None,
        )

        st.markdown(
            """
**Expected Result:** `ESCALATE` - 命中高疼痛 / 当前出血规则 → 升级给医生处理。
"""
        )

st.divider()


# ============================================================
# Main Layout
#
# Patient
#
# Staff workspace:
#   Staff chat | AI Copilot
# ============================================================

patient_col, staff_workspace_col = st.columns(
    [1, 2],
    gap="large",
)


# ============================================================
# LEFT
# Patient UI
# ============================================================

with patient_col:

    st.subheader("📱 患者端")

    st.caption(
        "模拟患者微信 / 企业微信会话"
    )

    with st.container(
        border=True,
        height=600,
    ):

        for message in st.session_state.messages:

            if message["role"] == "clinic":

                with st.chat_message(
                    "assistant",
                    avatar="👩‍💼",
                ):
                    st.write(
                        message["content"]
                    )

            elif message["role"] == "patient":

                with st.chat_message(
                    "user",
                    avatar="👴🏻",
                ):
                    st.write(
                        message["content"]
                    )

    # --------------------------------------------------------
    # Patient Input
    # --------------------------------------------------------

    with st.form(
        "patient_form",
        clear_on_submit=True,
    ):

        patient_reply = st.text_area(
            "患者回复",
            placeholder=(
                "例如：现在疼痛3分，没有出血，"
                "有一点肿，没有发烧。"
            ),
            height=100,
            label_visibility="collapsed",
        )

        patient_send = st.form_submit_button(
            "患者发送",
            type="primary",
            use_container_width=True,
        )

    if patient_send and patient_reply.strip():

        patient_reply = patient_reply.strip()

        # 先写入聊天记录
        st.session_state.messages.append(
            {
                "role": "patient",
                "content": patient_reply,
            }
        )

        st.session_state.last_error = None

        try:

            run_graph(patient_reply)

        except Exception as exc:

            st.session_state.last_error = str(exc)

        st.rerun()


# ============================================================
# RIGHT
# Staff Workspace
# ============================================================

with staff_workspace_col:

    st.subheader("💼 咨询师企微页面")

    st.caption(
        "企业微信聊天窗口 + AI Copilot 侧边栏"
    )

    staff_chat_col, copilot_col = st.columns(
        [1.1, 1],
        gap="medium",
    )


    # ========================================================
    # Staff Chat Window
    # ========================================================

    with staff_chat_col:

        st.markdown(
            "#### 💬 咨询师聊天窗口"
        )

        with st.container(
            border=True,
            height=600,
        ):

            for message in st.session_state.messages:

                # Patient message
                if message["role"] == "patient":

                    with st.chat_message(
                        "assistant",
                        avatar="👴🏻",
                    ):
                        st.write(
                            message["content"]
                        )

                # Clinic / consultant message
                elif message["role"] == "clinic":

                    with st.chat_message(
                        "user",
                        avatar="👩‍💼",
                    ):
                        st.write(
                            message["content"]
                        )


    # ========================================================
    # AI Copilot
    # ========================================================

    with copilot_col:

        st.markdown(
            "#### ✨ AI Copilot"
        )

        result = st.session_state.latest_result

        # ----------------------------------------------------
        # Error
        # ----------------------------------------------------

        if st.session_state.last_error:

            st.error(
                "Graph execution failed:\n\n"
                + st.session_state.last_error
            )

        # ----------------------------------------------------
        # No result yet
        # ----------------------------------------------------

        if result is None:

            with st.container(border=True):

                st.info(
                    "等待患者回复后，"
                    "AI 分析结果会显示在这里。"
                )

        # ----------------------------------------------------
        # AI Result
        # ----------------------------------------------------

        else:

            with st.container(border=True):

                # Latest patient reply

                st.markdown(
                    "**患者最新回复**"
                )

                st.write(
                    result.get(
                        "patient_reply",
                        ""
                    )
                )

                st.divider()

                # --------------------------------------------
                # Extraction
                # --------------------------------------------

                st.markdown(
                    "**AI 信息提取**"
                )

                feedback = {
                    "疼痛评分":
                        result.get("pain_score"),

                    "当前出血":
                        result.get(
                            "current_bleeding"
                        ),

                    "近期出血":
                        result.get(
                            "recent_bleeding"
                        ),

                    "肿胀":
                        result.get("swelling"),

                    "发热":
                        result.get("fever"),
                }

                st.json(feedback)

                st.divider()

                # --------------------------------------------
                # Policy
                # --------------------------------------------

                st.markdown(
                    "**Policy 判断**"
                )

                action = result.get(
                    "action"
                )

                if action == "NORMAL":

                    st.success(
                        "NORMAL"
                    )

                elif action == "ASK_MORE":

                    st.warning(
                        "ASK_MORE"
                    )

                elif action == "ESCALATE":

                    st.error(
                        "ESCALATE"
                    )

                else:

                    st.write(action)

                # --------------------------------------------
                # Rules
                # --------------------------------------------

                st.markdown(
                    "**Matched Rules**"
                )

                st.write(
                    result.get(
                        "matched_rules"
                    ) or []
                )

                # --------------------------------------------
                # Missing Fields
                # --------------------------------------------

                st.markdown(
                    "**Missing Fields**"
                )

                st.write(
                    result.get(
                        "missing_fields"
                    ) or []
                )

                # --------------------------------------------
                # Doctor Notification
                # --------------------------------------------

                doctor_notification = (
                    result.get(
                        "doctor_notification"
                    )
                )

                if doctor_notification:

                    st.divider()

                    st.markdown(
                        "**🚨 医生通知**"
                    )

                    st.error(
                        doctor_notification
                    )


        # ====================================================
        # Suggested Reply
        # ====================================================

        if st.session_state.draft_reply:

            st.markdown(
                "#### AI 建议回复"
            )

            edited_reply = st.text_area(
                "咨询师可编辑后发送",
                value=st.session_state.draft_reply,
                height=180,
                key="staff_reply_editor",
            )

            send_to_patient = st.button(
                "发送给患者",
                type="primary",
                use_container_width=True,
            )

            if send_to_patient:

                final_reply = (
                    edited_reply.strip()
                )

                if final_reply:

                    # 只有咨询师点击发送后
                    # 才进入真正聊天记录
                    st.session_state.messages.append(
                        {
                            "role": "clinic",
                            "content": final_reply,
                        }
                    )

                    st.session_state.draft_reply = ""

                    st.rerun()


        # ====================================================
        # Debug
        # ====================================================

        with st.expander(
            "Workflow State"
        ):

            st.write(
                "Thread ID:",
                st.session_state.thread_id,
            )

            st.write(
                "Waiting for patient:",
                st.session_state.waiting_for_patient,
            )

            if st.session_state.latest_result:

                st.json(
                    {
                        key: value
                        for key, value
                        in st.session_state.latest_result.items()
                        if key != "__interrupt__"
                    }
                )