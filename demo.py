import streamlit as st
import pandas as pd
import numpy as np

st.header("电荷电量表达式为:")
st.latex(
    r"q = \frac{18\pi}{\sqrt{2(\rho_1 - \rho_2)g}} \left(\frac{\eta l}{t(1 + \frac{b}{pr})}\right)^{\frac{3}{2}} \frac{d}{U}")

data = [{
    "空气压强 Pa": 1.01325 * 10 ** 5,
    "修正常数 N/m": 8.23 * 10 ** -3,
    "粘滞系数 kg·m^-1·s^-1": 1.83 * 10 ** -5,
    "平行极板间距离 m": 5.00 * 10 ** -3
}]
param1 = pd.DataFrame(data)
param1 = st.data_editor(
    param1,
    column_config={
        "空气压强 Pa": st.column_config.NumberColumn(
            "空气压强 Pa",
            help="空气压强 Pa",
            format="%.5e",
        ),
        "修正常数 N/m": st.column_config.NumberColumn(
            "修正常数 N/m",
            help="修正常数 N/m",
            format="%.2e",
        ),
        "粘滞系数 kg·m^-1·s^-1": st.column_config.NumberColumn(
            "粘滞系数 kg·m^-1·s^-1",
            help="粘滞系数 kg·m^-1·s^-1",
            format="%.2e",
        ),
        "平行极板间距离 m": st.column_config.NumberColumn(
            "平行极板间距离 m",
            help="平行极板间距离 m",
            format="%.2e",
        ),
    },
    hide_index=True,
    use_container_width=True
)
data = [{
    "下落距离 m": 1.6 * 10 ** -3,
    "重力加速度 m/s^2": 9.794,
    "油的密度 kg·m^-3 (20°C)": 981,
    "空气密度 kg·m^-3": 1.2928
}]
param2 = pd.DataFrame(data)
param2 = st.data_editor(
    param2,
    column_config={
        "下落距离 m": st.column_config.NumberColumn(
            "下落距离 m",
            help="下落距离 m",
            format="%.1e",
        ),
        "重力加速度 m/s^2": st.column_config.NumberColumn(
            "重力加速度 m/s^2",
            help="重力加速度 m/s^2",
            format="%.3f",
        ),
        "油的密度 kg·m^-3 (20°C)": st.column_config.NumberColumn(
            "油的密度 kg·m^-3 (20°C)",
            help="油的密度 kg·m^-3 (20°C)",
            format="%d",
        ),
        "空气密度 kg·m^-3": st.column_config.NumberColumn(
            "空气密度 kg·m^-3",
            help="空气密度 kg·m^-3",
            format="%.4f",
        ),
    },
    hide_index=True,
    use_container_width=True
)
st.divider()
st.subheader("数据输入区域")
data = {
    'U': [],
    't': []
}
param_input = pd.DataFrame(data)
param_input = st.data_editor(param_input, use_container_width=True, num_rows="dynamic",
                             column_config={
                                 "U": st.column_config.NumberColumn(
                                     "U",
                                     help="电压"
                                 ),
                                 "t": st.column_config.NumberColumn(
                                     "t",
                                     help="时间"
                                 ),
                             }
                             )


def calculate_q(U, t, rho1, rho2, g, eta, l, b, p, d):
    v = l / t
    r = np.sqrt(9 * eta * v / (2 * (rho1 - rho2) * g))
    # print(f"U:{U},t:{t}")

    numerator = 18 * np.pi

    # 计算分母
    denominator = np.sqrt(2 * (rho1 - rho2) * g)

    # 计算括号内的部分
    bracket_part = ((eta * l) / (t * (1 + b / (p * r)))) ** (3 / 2)

    # 计算q
    q = (numerator / denominator) * (bracket_part * d / U)

    return q


pwd = st.text_input("请输入软件密码: ", type='password')
p = ["96f0a81e13b6d23ecaa4a1db8322a28b", "123"]
count = 0
if st.button("计算") and (pwd in p):
    count += 1
    rho1 = param2["油的密度 kg·m^-3 (20°C)"].values[0]
    rho2 = param2["空气密度 kg·m^-3"].values[0]
    g = param2["重力加速度 m/s^2"].values[0]
    eta = param1["粘滞系数 kg·m^-1·s^-1"].values[0]
    l = param2["下落距离 m"].values[0]
    b = param1["修正常数 N/m"].values[0]
    p = param1["空气压强 Pa"].values[0]
    d = param1["平行极板间距离 m"].values[0]
    # st.write(rho1, rho2, g, eta, l, b, p, d)
    result = param_input.apply(lambda x: calculate_q(x[0], x[1], rho1, rho2, g, eta, l, b, p, d), axis=1)
    result = result.to_frame()
    result.reset_index(names=["测试序号"], inplace=True)
    result.rename(columns={0: "电荷量q"}, inplace=True)
    result["电子数"] = (result["电荷量q"] // (1.6 * 10 ** -19))
    result["单电子电荷量"] = result["电荷量q"] / (result["电荷量q"] // (1.6 * 10 ** -19))
    # print(result)
    result["相对误差"] = np.abs((result["单电子电荷量"] - 1.60217733 * 10 ** -19) / (1.60217733 * 10 ** -19)) * 100
    st.divider()

    st.data_editor(result, use_container_width=True, hide_index=True,
                   column_config={
                       "电荷量q": st.column_config.NumberColumn(
                           "电荷量q",
                           help="电荷量q",
                           format="%.5e",
                       ),
                       "单电子电荷量": st.column_config.NumberColumn(
                           "单电子电荷量",
                           help="单电子电荷量",
                           format="%.5e",
                       ),
                       "相对误差": st.column_config.NumberColumn(
                           "相对误差",
                           help="相对误差",
                           format="%.2f %%",
                       ),
                   }
                   )
elif count != 0:
    st.write("密码错误！！！！")
else:
    count += 1
