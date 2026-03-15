import streamlit as st

# 設定網頁標題與排版
st.set_page_config(page_title="ADA 標準 DKA/HHS 導航系統", layout="centered", page_icon="🚨")

st.title("🚨 ADA 標準 DKA/HHS 動態導航系統 (究極安全版)")
st.markdown("**基於美國糖尿病學會 (ADA) 高血糖危機處置指引，並內建極端數值防護演算法**")
st.caption("配方預設：Regular Insulin 或 速效 Insulin 100U + 0.9% N/S 100mL (1 U/mL = 1 mL/hr = 1 U/hr)")

# 選擇疾病型態 (決定防護轉換點)
disease_type = st.radio(
    "👉 請選擇病患的疾病型態：",
    ["DKA (糖尿病酮酸血症) - 轉換點 200", "HHS (高滲透壓高血糖狀態) - 轉換點 300"],
    horizontal=True
)

tab1, tab2 = st.tabs(["Phase 1: 初始評估與給藥 (Initial)", "Phase 2: 動態滴定與轉換 (Titration)"])

# ==========================================
# 第一分頁：Phase 1 初始評估 (ADA 標準 + 雙係數血鈉)
# ==========================================
with tab1:
    st.header("Phase 1: 初始給藥與輸液評估")
    
    col1, col2 = st.columns(2)
    with col1:
        weight_p1 = st.number_input("病患體重 (kg)", min_value=30.0, max_value=200.0, value=60.0, step=1.0, key="w1")
        init_gluc = st.number_input("初始血糖 (mg/dL)", min_value=50, max_value=2000, value=450, step=10, key="g1")
        ph_val = st.number_input("動脈/靜脈 pH 值", min_value=6.0, max_value=7.5, value=7.1, step=0.01, key="ph1")

    with col2:
        init_k = st.number_input("初始血鉀 K+ (mEq/L)", min_value=1.0, max_value=10.0, value=4.0, step=0.1, key="k1")
        init_na = st.number_input("測量血鈉 Na+ (mEq/L)", min_value=100, max_value=200, value=135, step=1, key="na1")

    if st.button("計算 ADA 初始醫囑", type="primary", key="btn1"):
        st.divider()
        
        # 1. 初始點滴復甦
        st.subheader("💧 1. 初始液體復甦 (第一小時)")
        st.info("優先給予 **0.9% NaCl** (或平衡性晶體輸液如 LR) **1000 - 1500 mL/hr** 快速滴注。\n\n*(※ 警語：若病患有心/腎衰竭，請醫師重新評估給水量)*")

        # 2. 血鉀 Hard Stop 
        st.subheader("🛑 2. 血鉀檢核 (Potassium Check)")
        if init_k < 3.3:
            st.error(f"**絕對禁忌：血鉀 {init_k} < 3.3 mEq/L！**\n\n**HOLD INSULIN (禁止啟動胰島素)！**\n請先由靜脈補充 KCl 20-30 mEq/hr，直到 K+ ≥ 3.3。")
        elif 3.3 <= init_k <= 5.3:
            st.success(f"**血鉀 {init_k} mEq/L：安全範圍。**\n\n允許啟動 Insulin。於每公升點滴中加入 **20-30 mEq KCl** (目標維持血鉀 4.0-5.0)。")
        else:
            st.warning(f"**血鉀 {init_k} mEq/L：偏高。**\n\n允許啟動 Insulin。點滴**暫不加鉀**，請 Q2H 嚴密追蹤。")

        # 3. 校正血鈉 (導入 1999 Hillier 雙係數防護)
        st.subheader("🧪 3. 維持輸液選擇 (第二小時起)")
        if init_gluc <= 400:
            corr_na = init_na + 1.6 * ((init_gluc - 100) / 100)
            factor_used = "1.6 (傳統 Katz 公式)"
        else:
            corr_na = init_na + 2.4 * ((init_gluc - 100) / 100)
            factor_used = "2.4 (Hillier 重症精確公式)"
            
        st.markdown(f"依據血糖值，系統採用係數 **{factor_used}**，計算出「校正血鈉」為：**{corr_na:.1f} mEq/L**")
        
        if corr_na >= 135:
            st.warning("👉 判斷：血鈉正常或偏高 (嚴重缺乏游離水)。\n\n處置：維持點滴改掛 **0.45% NaCl** (250-500 mL/hr)。")
        else:
            st.success("👉 判斷：血鈉偏低。\n\n處置：維持點滴續掛 **0.9% NaCl** (250-500 mL/hr)。")

        # 4. ADA Insulin 給藥指引
        st.subheader("💉 4. 胰島素初始給藥 (雙軌選擇)")
        if init_k >= 3.3:
            bolus = weight_p1 * 0.1
            rate_opt1 = weight_p1 * 0.1
            rate_opt2 = weight_p1 * 0.14
            st.info(f"""
            **ADA 建議以下兩種作法擇一 (A級實證)：**
            * **作法 A (有 Bolus)**：先給予 IV Bolus **{bolus:.1f} U**，隨後設定 Pump 速率 **{rate_opt1:.1f} mL/hr** (0.1 U/kg/hr)。
            * **作法 B (無 Bolus)**：直接設定 Pump 速率 **{rate_opt2:.1f} mL/hr** (0.14 U/kg/hr)。
            """)

        # 5. 酸鹼平衡 
        st.subheader("🩺 5. 酸鹼平衡 (Bicarbonate)")
        if ph_val < 6.9:
            st.error(f"**pH {ph_val} < 6.9：極度酸血症！**\n\nADA 建議：給予 100 mmol NaHCO3 加入 400 mL 無菌水中 (內含 20 mEq KCl)，以 2 小時滴注。Q2H 追蹤直至 pH ≥ 7.0。")
        else:
            st.success(f"**pH {ph_val} ≥ 6.9**：依據 ADA 指引，**不建議**常規給予碳酸氫鈉 (NaHCO3)。")


# ==========================================
# 第二分頁：Phase 2 動態滴定 (加入三大極端防護墊)
# ==========================================
with tab2:
    st.header("Phase 2: Pump 動態滴數調整 (Q1H)")
    
    col3, col4 = st.columns(2)
    with col3:
        weight_p2 = st.number_input("病患體重 (kg)", min_value=30.0, max_value=200.0, value=60.0, step=1.0, key="w2")
        old_gluc = st.number_input("前一小時血糖 (mg/dL)", min_value=20, max_value=1500, value=300, step=10, key="g2_old")

    with col4:
        new_gluc = st.number_input("最新血糖 (mg/dL)", min_value=20, max_value=1500, value=250, step=10, key="g2_new")
        current_rate = st.number_input("目前 Pump 速率 (mL/hr)", min_value=0.0, max_value=50.0, value=6.0, step=0.5, key="r2")

    if st.button("計算 ADA 最新滴數", type="primary", key="btn2"):
        st.divider()
        
        target_threshold = 200 if "DKA" in disease_type else 300
        target_range = "150-200" if "DKA" in disease_type else "200-300"
        drop = old_gluc - new_gluc
        
        # 危機處理：嚴重低血糖
        if new_gluc < 70:
            st.error("🆘 **嚴重低血糖 (< 70 mg/dL)！**\n\n立刻關閉 Insulin Pump！給予 D50W 推注，並改為 Q15min 密切監測。")
        
        # 防護轉換期 (ADA 目標：DKA <= 200, HHS <= 300)
        elif new_gluc <= target_threshold:
            min_rate = max(0.5, weight_p2 * 0.02)
            max_rate = weight_p2 * 0.05
            half_rate = max(min_rate, current_rate / 2) # 加入地板值防護
            
            st.error(f"🚨 **ADA 關鍵防護期**：{disease_type} 血糖已達 {new_gluc} mg/dL！\n\n必須**立刻同時**執行以下兩項：")
            st.warning("1. **加糖**：維持點滴立即加入 5% 葡萄糖 (改為 **D5W + 0.45% NaCl** 或 D5W + 0.9% NaCl)。")
            st.warning(f"2. **降速**：將 Insulin 速率調降至 0.02-0.05 U/kg/hr。建議直接將原速率減半為 **{half_rate:.1f} mL/hr** (系統已鎖定最低安全底線 {min_rate:.1f} mL/hr)。")
            st.info(f"🎯 **後續 ADA 目標**：精準微調點滴與 Pump，將血糖穩定鎖定在 **{target_range} mg/dL** 之間，直到酸中毒解除。")
            
        # 正常動態調整
        else:
            st.write(f"過去一小時血糖降幅：**{drop:.0f} mg/dL**")
            
            # 【防護 1】懸崖趨勢預警 (Look-ahead Warning)
            if (new_gluc <= target_threshold + 50) and (drop > 75):
                st.warning(f"⚠️ **邊界趨勢預警**：血糖已降至 {new_gluc}，且降速極快！下一小時極可能跌破防護線 ({target_threshold})，請預先準備好含糖輸液 (D5W)。")

            if drop < 50:
                doubled_rate = current_rate * 2
                # 【防護 2】指數爆炸天花板 (Ceiling Limit)
                if doubled_rate > 15.0:
                    st.error(f"🛑 **異常警告：滴數已達安全上限 ({doubled_rate:.1f} mL/hr)！**\n\n系統拒絕繼續無限制加倍。請強烈懷疑 **IV 管路漏針 (Infiltration)** 或阻塞！請重新建立靜脈管路並請醫師重新評估。")
                else:
                    st.warning(f"📉 **降幅 < 50 mg/dL (降太慢)**：\n\nADA 指引建議：若降幅未達標，應將連續輸注速率**加倍 (Double)**。\n\n👉 建議新滴數：**{doubled_rate:.1f} mL/hr**")
            
            elif 50 <= drop <= 75:
                st.success(f"✨ **降幅 50-75 mg/dL (完美符合 ADA 目標)**：\n\n👉 處置：維持原速率不動，繼續 Q1H 監測。\n\n🎯 **維持滴數：{current_rate:.1f} mL/hr**")
            
            else:
                adjust = weight_p2 * 0.05
                # 【防護 3】負數地板值 (Floor Limit)
                min_allowed = max(0.5, weight_p2 * 0.02)
                new_rate = max(min_allowed, current_rate - adjust)
                
                st.warning(f"📉 **降幅 > 75 mg/dL (降太快)**：\n\n為避免劇烈血糖波動，建議適度調降 Pump 速率。\n\n👉 建議新滴數：**{new_rate:.1f} mL/hr** (系統已自動設定安全底線為 {min_allowed:.1f})")

# --- 版權聲明 ---
st.divider()
st.caption("© 2026 ER DKA/HHS Clinical Decision Support Tool. All Rights Reserved. \n\n本系統採 CC BY-NC-ND 4.0 授權，僅供臨床決策輔助與教學使用，不可取代醫師最終專業判斷。")
st.caption("© 2026 [護理師 吳智弘] 開發設計. 版權所有。")
