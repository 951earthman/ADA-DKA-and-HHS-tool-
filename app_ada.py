import streamlit as st
# ==========================================
# 側邊欄：臨床生理與機轉小寶典 (Just-in-Time Learning)
# ==========================================
with st.sidebar:
    st.header("📚 臨床機轉小寶典")
    st.caption("輸入關鍵字，快速複習急診重症生理機轉。")
    
    # 搜尋列設計
    search_query = st.text_input("🔍 搜尋關鍵字 (例：酮體, 鉀, 腦水腫, 鈉)...", "").strip().lower()
    
    # 建立知識庫字典 (Knowledge Base)
    knowledge_base = {
        "DKA 為什麼會變酸？ (機轉)": """
        **【絕對缺乏胰島素】**
        當體內完全沒有胰島素時，葡萄糖無法進入細胞。細胞「以為」身體在挨餓，於是開始瘋狂**分解脂肪**來當作能量。
        脂肪分解的副產物就是**「酮體 (Ketones)」**，這是一種強酸，會在血液中大量堆積，造成高陰離子間隙代謝性酸中毒 (High Anion Gap Metabolic Acidosis)。
        👉 *處置重點：打 Insulin 不是為了降血糖，是為了停止脂肪分解、關閉酮體製造工廠！*
        """,
        
        "HHS 為什麼會極度脫水？ (機轉)": """
        **【相對缺乏胰島素】**
        病患體內還有「微量」的胰島素，這些量剛好足夠阻止脂肪大量分解（所以不太會產生酮體和酸中毒）。
        但是，這點胰島素不足以把血糖送進細胞。血糖於是飆高到 600、800 甚至破千。超高血糖會從腎臟引發強烈的**「滲透壓性利尿 (Osmotic Diuresis)」**，把體內的水分大量排光。
        👉 *處置重點：HHS 的病患通常缺水高達 9-10 公升，前期「大量灌注生理食鹽水 (0.9% N/S)」甚至比打 Insulin 更重要！*
        """,
        
        "致命陷阱：血鉀的捉迷藏 (K+ Shift)": """
        **【為什麼抽血鉀很高，卻不能打 Insulin？】**
        在嚴重酸血症時，血液裡充滿氫離子 (H+)。身體為了代償，會把 H+ 塞進細胞內，同時把細胞內的**鉀離子 (K+) 趕出來**到血液中。
        所以，**抽血看到的血鉀正常或偏高，其實是「假象」**！病人全身的「總鉀量」其實是嚴重缺乏的（都被尿液排掉了）。
        一旦你打了 Insulin，Insulin 會像搬運工一樣，瞬間把血液中的 K+ 全部掃回細胞內。如果原本血鉀就不高 (< 3.3)，這瞬間的轉移會引發**致命性低血鉀與心律不整**。
        """,
        
        "為什麼會有假性低血鈉？ (校正公式)": """
        **【高血糖的稀釋效應】**
        血管裡極高的葡萄糖，會產生巨大的「滲透壓」，把細胞內的水分強力「吸」進血管裡。
        血管裡的水變多了，原本的血鈉濃度就被「稀釋」了。這就是為什麼 DKA/HHS 病人抽血常看到 Na 125、128 的原因。
        👉 *我們必須用 1.6 或 2.4 的常數去「還原」真實的血鈉，才能準確判斷病患到底是缺水還是缺鈉，進而決定要給 0.45% 還是 0.9% 的點滴。*
        """,
        
        "防護期：預防腦水腫 (Cerebral Edema)": """
        **【為什麼 200/300 就要加糖水？】**
        高血糖時，腦細胞為了適應血管外的高滲透壓，會自己在細胞內製造「滲透壓物質」來抗衡，避免腦袋萎縮。
        如果在急診，我們用 Insulin 把血糖**降得太快、太低**，血管內的滲透壓會瞬間暴跌。這時，腦細胞內相對處於「高滲透壓」狀態，水分會瘋狂灌進腦細胞，引發**致命性腦水腫**。
        👉 *這就是為什麼 HHS 必須在 300 mg/dL 就提早踩煞車（加 D5W），給腦細胞慢慢適應的時間。*
        """
    }

    # 根據搜尋列過濾並顯示內容
    found = False
    for title, content in knowledge_base.items():
        # 如果搜尋列是空的，或者關鍵字有在標題/內容中，就顯示出來
        if search_query == "" or search_query in title.lower() or search_query in content.lower():
            found = True
            with st.expander(title):
                st.markdown(content)
                
    if not found:
        st.warning("找不到相關內容，請嘗試其他關鍵字！")
# ==========================================

# 設定網頁標題與排版
st.set_page_config(page_title="ADA 標準 DKA/HHS 導航系統", layout="centered", page_icon="🚨")

st.title("🚨 ADA 標準 DKA/HHS 動態導航系統 (頂配安全版)")
st.markdown("**基於美國糖尿病學會 (ADA) 高血糖危機處置指引，內建滲透壓與動態血鉀防護**")
st.caption("配方預設：Regular 或 速效 Insulin 100U + 0.9% N/S 100mL (1 U/mL = 1 mL/hr = 1 U/hr)")

# 選擇疾病型態 (決定防護轉換點)
disease_type = st.radio(
    "👉 請選擇病患的疾病型態：",
    ["DKA (糖尿病酮酸血症) - 轉換點 200", "HHS (高滲透壓高血糖狀態) - 轉換點 300"],
    horizontal=True
)

tab1, tab2 = st.tabs(["Phase 1: 初始評估與給藥 (Initial)", "Phase 2: 動態滴定與轉換 (Titration)"])

# ==========================================
# 第一分頁：Phase 1 初始評估
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
        
        # 0. 血液滲透壓評估 (Effective Osmolality)
        st.subheader("🧠 0. 有效血液滲透壓 (Effective Osmolality)")
        eff_osmo = (2 * init_na) + (init_gluc / 18)
        st.markdown(f"系統依據 (2 × Na + Glucose/18) 計算，有效滲透壓為：**{eff_osmo:.1f} mOsm/kg**")
        if eff_osmo > 320:
            st.error("🚨 **診斷提示：滲透壓 > 320 mOsm/kg！**\n\n此為典型 HHS 超高滲透壓狀態。病患神經學症狀（如意識改變）與此高度相關，前期需極度積極補充水分。")
        else:
            st.info("💡 滲透壓 ≤ 320 mOsm/kg。若病患有嚴重意識不清，請同步排除其他非高血糖神經學因素。")

        # 1. 初始點滴復甦
        st.subheader("💧 1. 初始液體復甦 (第一小時)")
        st.info("優先給予 **0.9% NaCl** (或平衡性晶體輸液如 LR) **1000 - 1500 mL/hr** 快速滴注。\n*(警語：若病患有心/腎衰竭，請醫師重新評估給水量)*")

        # 2. 血鉀 Hard Stop 
        st.subheader("🛑 2. 血鉀檢核 (Potassium Check)")
        if init_k < 3.3:
            st.error(f"**絕對禁忌：血鉀 {init_k} < 3.3 mEq/L！**\n\n**HOLD INSULIN (禁止啟動胰島素)！**\n請先由靜脈補充 KCl 20-30 mEq/hr，直到 K+ ≥ 3.3。")
        elif 3.3 <= init_k <= 5.3:
            st.success(f"**血鉀 {init_k} mEq/L：安全範圍。**\n\n允許啟動 Insulin。於每公升點滴中加入 **20-30 mEq KCl** (目標維持血鉀 4-5)。")
        else:
            st.warning(f"**血鉀 {init_k} mEq/L：偏高。**\n\n允許啟動 Insulin。點滴**暫不加鉀**，請嚴密追蹤。")

        # 3. 校正血鈉 (Hillier 雙係數)
        st.subheader("🧪 3. 維持輸液選擇 (第二小時起)")
        factor_used = 1.6 if init_gluc <= 400 else 2.4
        corr_na = init_na + factor_used * ((init_gluc - 100) / 100)
            
        st.markdown(f"系統採用 **{factor_used}** 係數計算，校正血鈉為：**{corr_na:.1f} mEq/L**")
        if corr_na >= 135:
            st.warning("👉 處置：維持點滴改掛 **0.45% NaCl** (250-500 mL/hr)，以補充游離水。")
        else:
            st.success("👉 處置：維持點滴續掛 **0.9% NaCl** (250-500 mL/hr)。")

        # 4. ADA Insulin 給藥指引
        st.subheader("💉 4. 胰島素初始給藥 (雙軌選擇)")
        if init_k >= 3.3:
            st.info(f"**ADA 建議兩種作法擇一 (A級實證)：**\n* **作法 A**：IV Bolus **{(weight_p1 * 0.1):.1f} U**，隨後 Pump 設定 **{(weight_p1 * 0.1):.1f} mL/hr**。\n* **作法 B**：無 Bolus，直接設定 Pump **{(weight_p1 * 0.14):.1f} mL/hr**。")

        # 5. 酸鹼平衡 
        st.subheader("🩺 5. 酸鹼平衡 (Bicarbonate)")
        if ph_val < 6.9:
            st.error(f"**pH {ph_val} < 6.9：極度酸血症！**\n建議給予 100 mmol NaHCO3 加入無菌水中滴注。")
        else:
            st.success(f"**pH {ph_val} ≥ 6.9**：不建議常規給予碳酸氫鈉。")


# ==========================================
# 第二分頁：Phase 2 動態滴定 (加入動態血鉀檢核)
# ==========================================
with tab2:
    st.header("Phase 2: Pump 動態滴數調整 (Q1H/Q2H)")
    
    col3, col4 = st.columns(2)
    with col3:
        weight_p2 = st.number_input("病患體重 (kg)", min_value=30.0, max_value=200.0, value=60.0, step=1.0, key="w2")
        old_gluc = st.number_input("前次血糖 (mg/dL)", min_value=20, max_value=1500, value=300, step=10, key="g2_old")

    with col4:
        new_gluc = st.number_input("最新血糖 (mg/dL)", min_value=20, max_value=1500, value=250, step=10, key="g2_new")
        current_rate = st.number_input("目前 Pump 速率 (mL/hr)", min_value=0.0, max_value=50.0, value=6.0, step=0.5, key="r2")

    st.markdown("---")
    st.markdown("##### 🧪 動態血鉀安全檢核 (ADA 建議 Q2-4H 追蹤)")
    has_new_k = st.checkbox("有 4 小時內的最新血鉀 (K+) 報告", value=False)
    new_k = None
    if has_new_k:
        new_k = st.number_input("輸入最新血鉀 K+ (mEq/L)", min_value=1.0, max_value=10.0, value=4.0, step=0.1, key="k2")

    if st.button("計算 ADA 最新滴數", type="primary", key="btn2"):
        st.divider()
        
        # 【最高優先級攔截】：Phase 2 血鉀過低
        if has_new_k and new_k < 3.3:
            st.error(f"🛑 **動態血鉀攔截：最新血鉀 {new_k} < 3.3 mEq/L！**\n\n**必須立刻關閉 Insulin Pump！**\nInsulin 會導致血鉀持續進入細胞。請先靜脈補充 KCl 20-30 mEq/hr，待 K+ ≥ 3.3 後再重新啟動 Pump。")
            st.stop() # 程式在此停止，不給予任何滴數調整建議
        
        elif has_new_k and new_k > 5.3:
            st.warning(f"⚠️ **最新血鉀 {new_k} > 5.3 mEq/L**：請確認目前維持點滴中已**停止加入 KCl**，避免高血鉀。")
        elif has_new_k:
            st.success(f"✅ **最新血鉀 {new_k} mEq/L (安全)**：請確認目前維持點滴中持續加入 KCl 20-30 mEq/L。")
        else:
            st.info("🔔 **安全提醒**：未輸入最新血鉀。Insulin 會造成鉀離子快速消耗，請確認病患已安排 Q2-Q4H 的電解質追蹤。")

        st.markdown("---")
        
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
            half_rate = max(min_rate, current_rate / 2)
            
            st.error(f"🚨 **ADA 關鍵防護期**：{disease_type} 血糖已達 {new_gluc} mg/dL！\n\n必須**立刻同時**執行以下兩項：")
            st.warning("1. **加糖**：維持點滴立即加入 5% 葡萄糖 (改為 **D5W + 0.45% NaCl** 或 D5W + 0.9% NaCl)。")
            st.warning(f"2. **降速**：建議直接將原速率減半為 **{half_rate:.1f} mL/hr** (系統已鎖定最低安全底線 {min_rate:.1f} mL/hr)。")
            st.info(f"🎯 **後續 ADA 目標**：將血糖穩定鎖定在 **{target_range} mg/dL** 之間，直到酸中毒解除。")
            
        # 正常動態調整
        else:
            st.write(f"過去期間血糖降幅：**{drop:.0f} mg/dL**")
            
            if (new_gluc <= target_threshold + 50) and (drop > 75):
                st.warning(f"⚠️ **邊界趨勢預警**：血糖已降至 {new_gluc}，極可能即將跌破防護線 ({target_threshold})，請預先準備含糖輸液 (D5W)。")

            if drop < 50:
                doubled_rate = current_rate * 2
                if doubled_rate > 15.0:
                    st.error(f"🛑 **滴數已達安全上限 ({doubled_rate:.1f} mL/hr)！**\n請強烈懷疑 **IV 管路漏針 (Infiltration)** 或阻塞！請重新建立靜脈管路並請醫師評估。")
                else:
                    st.warning(f"📉 **降幅 < 50 mg/dL (降太慢)**：\nADA 建議將連續輸注速率**加倍 (Double)**。\n👉 建議新滴數：**{doubled_rate:.1f} mL/hr**")
            
            elif 50 <= drop <= 75:
                st.success(f"✨ **降幅 50-75 mg/dL (完美達標)**：\n👉 維持原速率不動，繼續監測。\n🎯 **維持滴數：{current_rate:.1f} mL/hr**")
            
            else:
                adjust = weight_p2 * 0.05
                min_allowed = max(0.5, weight_p2 * 0.02)
                new_rate = max(min_allowed, current_rate - adjust)
                
                st.warning(f"📉 **降幅 > 75 mg/dL (降太快)**：\n為避免劇烈血糖波動，建議適度調降 Pump 速率。\n👉 建議新滴數：**{new_rate:.1f} mL/hr**")

st.divider()
st.caption("© 2026 ER DKA/HHS Clinical Decision Support Tool. All Rights Reserved. \n\n本系統採 CC BY-NC-ND 4.0 授權，僅供臨床決策輔助與教學使用，不可取代醫師最終專業判斷。")
st.caption("© 2026 [護理師 吳智弘] 開發設計. 版權所有。")
