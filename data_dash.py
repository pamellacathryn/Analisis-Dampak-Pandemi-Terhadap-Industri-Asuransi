import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
from streamlit_option_menu import option_menu

st.markdown('<style>#vg-tooltip-element{z-index: 1000051}</style>', unsafe_allow_html=True)

# dataset
perusahaan = pd.read_csv('perusahaan.csv')
premi = pd.read_csv('pendapatan_premi.csv')
klaim = pd.read_csv('klaim_terbayar.csv')
premi["Total_premi"] = premi["LI_pendapatan_premi"]+premi["GI_pendapatan_premi"]+premi["RE_pendapatan_premi"]+premi["SI_pendapatan_premi"]+premi["MI_pendapatan_premi"]
klaim["Total_klaim"] = klaim["LI_klaim_terbayar"]+klaim["GI_klaim_terbayar"]+klaim["RE_klaim_terbayar"]+klaim["SI_klaim_terbayar"]+klaim["MI_klaim_terbayar"]
float_1 = pd.merge(premi, klaim, how='left', on='bulan')
float = pd.DataFrame(list(zip(
    float_1["bulan"],
    float_1["LI_pendapatan_premi"]-float_1["LI_klaim_terbayar"],
    float_1["GI_pendapatan_premi"]-float_1["GI_klaim_terbayar"],
    float_1["RE_pendapatan_premi"]-float_1["RE_klaim_terbayar"],
    float_1["SI_pendapatan_premi"]-float_1["SI_klaim_terbayar"],
    float_1["MI_pendapatan_premi"]-float_1["MI_klaim_terbayar"],
    float_1["Total_premi"]-float_1["Total_klaim"]
)), columns = ["bulan","LI_float","GI_float","RE_float","SI_float","MI_float","Total_float"])

with st.sidebar:
    st.header("Navigation")
    select = option_menu(
        menu_title=None,
        options=["Project","Glossary", "Links"],
        icons=["kanban","book","link"],
        styles={"nav-link":{"font-size":"14px"}}
    )
    st.header("About")
    st.info("This web app is made by Pamella Cathryn. You can follow me on [LinkedIn](https://linkedin.com/in/pamellacathryn) | [Instagram](https://instagram.com/pamellacathryn) | [GitHub](https://github.com/pamellacathryn)")



if select == "Project":
    # latar belakang
    st.markdown("<h1 style='text-align: center; '>Apakah Industri Asuransi di Indonesia Survive selama Pandemi?</h1>",
                unsafe_allow_html=True)
    st.markdown("<h6 style='text-align: center; '>111 Pamella Cathryn - DQLab Tetris Program Batch II</h6>",
                unsafe_allow_html=True)
    st.write("")
    st.header('Latar Belakang')
    kolom1, kolom2 = st.columns([1,2])
    with kolom1:
        st.image('Asuransi_jiwa_terbaik.jpg')
    kolom2.markdown('<div style="text-align: justify;">Bisnis asuransi merupakan bisnis yang menarik karena didasarkan pada ketidakpastian dengan derajat yang lebih tinggi. Beberapa orang memandang rendah praktik asuransi karena menganggap perusahaan asuransi berusaha \"mengkapitalisasi kehidupan\" seseorang. Namun, mereka yang menyadari betapa kejamnya ketidakpastian di masa depan cenderung akan mengamankan diri dan aset di asuransi.</div>', unsafe_allow_html=True)
    kolom2.markdown('<div style="text-align: justify;"></div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align: justify;">Perusahaan asuransi mendapat keuntungannya dengan menjual premi asuransi melebihi nilai pembayaran saat klaim. Selisih dari nilai premi yang dikumpulkan dengan klaim yang harus dibayarkan pada nasabah disebut dengan Insurance Float. Bagi sebagian perusahaan asuransi, float bulanan akan langsung dihitung dan dikumpulkan menjadi laba berbasis tahunan. Bagi sebagian lainnya, float ini kemudian digunakan untuk diinvestasikan yang memberikan keuntungan lebih. Dengan kata lain, insurance float merupakan sumber modal dari perusahaan asuransi untuk melakukan investasi.</div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align: justify;"></div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align: justify;">Terjadinya pandemi Covid-19 berdampak langsung pada sektor-sektor finansial, termasuk pada Industri Asuransi. Pandemi Covid-19 juga menyebabkan resesi global pada tahun 2020. Resesi ini merupakan resesi terburuk di dunia sejak tahun 1930-an. Hal inilah yang menyebabkan nasabah-nasabah ragu untuk menaruh uang mereka untuk membayar premi asuransi dan pemasukan perusahaan asuransi pun menurun. Pada Kesempatan ini, akan dilakukan analisis apakah Pandemi Covid-19 memengaruhi pemasukan insurance float Industri Asuransi secara signifikan.</div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align: justify;"></div>', unsafe_allow_html=True)
    st.markdown("""---""")
    st.header("Hasil Analisis")
    #pie chart
    col1, col2 = st.columns([2,3])
    with col1:
        # This is an example of a plotly pie chart
        fig = px.pie(perusahaan["jumlah"], values=perusahaan["jumlah"], names=perusahaan['jenis'])
        fig.update_traces(textposition='inside', textinfo='label+percent', showlegend=False)
        fig.update_layout(width=250, height=275,margin=dict(r=1,l=1,t=1,b=1))
        st.write(fig)
        st.write(" ")
    col2.markdown('<div style="text-align: justify;">Dikutip dari Badan Pusat Statistik, saat ini (per 31 Desember 2021) terdapat 149 unit perusahaan asuransi konvensional di Indonesia. Secara rinci, sebanyak 77 unit merupakan perusahaan asuransi umum, 60 unit perusahaan asuransi jiwa, 7 unit perusahaan reasuransi, 2 unit perusahaan penyelenggara program asuransi sosial dan jaminan sosial tenaga kerja, serta 3 perusahaan sisanya merupakan penyelenggara asuransi untuk PNS dan TNI/Polri.</div>', unsafe_allow_html=True)

    #linechart function
    def get_chart(data):
        hover = alt.selection_single(
            fields=["bulan"],
            nearest=True,
            on="mouseover",
            empty="none",
        )
        lines = (
            alt.Chart(data)
            .mark_line()
            .encode(
                x="bulan",
                y=alt.Y("in Millions Rupiah", title="in Millions Rupiah"),
                color=alt.Color("Legend", sort=['Premi Bruto'], scale=alt.Scale(range=["#01AEC6", "#F4A261"]))
            )
        )
        points = lines.transform_filter(hover).mark_circle(size=65)
        tooltips = (
            alt.Chart(data)
            .mark_rule()
            .encode(
                x="bulan",
                y="in Millions Rupiah",
                opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
                tooltip=[
                    alt.Tooltip("bulan", title="Bulan"),
                    alt.Tooltip("in Millions Rupiah", title="Value"),
                ],
            )
            .add_selection(hover)
        )
        xrule = alt.Chart(data).mark_rule().encode(
            x=alt.Y('bulan_covid', title="Bulan"),
            size=alt.value(1),
            color=alt.value("#f69697"),
        )
        return (lines + points + tooltips + xrule).interactive()

    choose = st.selectbox(
            'Jenis Asuransi:',
            ('Life Insurance', 'General Insurance', 'Reinsurance', 'Social Insurance', 'Mandatory Insurance','Total'))
    st.write("")

    st.markdown("<h4 style='text-align: center; '>Statistika Deskriptif</h4>", unsafe_allow_html=True)
    kolumn1, kolumn2, kolumn3 = st.columns([1,3,1])
    if choose == 'Life Insurance':
        df = pd.DataFrame(list(zip(premi["LI_pendapatan_premi"], klaim["LI_klaim_terbayar"], float["LI_float"])), columns=["Premi Bruto", "Klaim Bruto","Insurance Float"])
    elif choose == 'General Insurance':
        df = pd.DataFrame(list(zip(premi["GI_pendapatan_premi"], klaim["GI_klaim_terbayar"], float["GI_float"])), columns=["Premi Bruto", "Klaim Bruto","Insurance Float"])
    elif choose == 'Reinsurance':
        df = pd.DataFrame(list(zip(premi["RE_pendapatan_premi"], klaim["RE_klaim_terbayar"], float["RE_float"])), columns=["Premi Bruto", "Klaim Bruto","Insurance Float"])
    elif choose == 'Social Insurance':
        df = pd.DataFrame(list(zip(premi["SI_pendapatan_premi"], klaim["SI_klaim_terbayar"], float["SI_float"])), columns=["Premi Bruto", "Klaim Bruto","Insurance Float"])
    elif choose == 'Mandatory Insurance':
        df = pd.DataFrame(list(zip(premi["MI_pendapatan_premi"], klaim["MI_klaim_terbayar"], float["MI_float"])), columns=["Premi Bruto", "Klaim Bruto","Insurance Float"])
    elif choose == 'Total':
        df = pd.DataFrame(list(zip(premi["Total_premi"], klaim["Total_klaim"], float["Total_float"])), columns=["Premi Bruto", "Klaim Bruto", "Insurance Float"])
    with kolumn2:
        st.write(df.describe())

    #line chart
    st.markdown("<h4 style='text-align: center; '>Perkembangan Premi dan Klaim 2016-2021</h4>", unsafe_allow_html=True)
    line_data1 = premi.copy()
    line_data1["bulan"] = pd.to_datetime(line_data1["bulan"])
    line_data1["bulan_covid"] = [pd.to_datetime("2020-03-01") for i in range(len(line_data1))]
    line_data2 = klaim.copy()
    line_data2["bulan"] = pd.to_datetime(line_data2["bulan"])
    line_data2["bulan_covid"] = [pd.to_datetime("2020-03-01") for i in range(len(line_data2))]
    if choose == 'Life Insurance':
        data1 = pd.DataFrame(list(zip(line_data1["bulan"], line_data1["LI_pendapatan_premi"], line_data2["LI_klaim_terbayar"])),
                             columns=["bulan", "Premi Bruto", "Klaim Bruto"])
        data1_melted = pd.melt(data1, id_vars=['bulan'], var_name='Legend', value_name='in Millions Rupiah')
        data1_melted["bulan_covid"] = [pd.to_datetime("2020-03-01") for i in range(len(data1_melted))]
        data = data1_melted
        posisi = -220
    elif choose == 'General Insurance':
        data2 = pd.DataFrame(list(zip(line_data1["bulan"], line_data1["GI_pendapatan_premi"], line_data2["GI_klaim_terbayar"])),
                             columns=["bulan", "Premi Bruto", "Klaim Bruto"])
        data2_melted = pd.melt(data2, id_vars=['bulan'], var_name='Legend', value_name='in Millions Rupiah')
        data2_melted["bulan_covid"] = [pd.to_datetime("2020-03-01") for i in range(len(data2_melted))]
        data = data2_melted
        posisi = -220
    elif choose == 'Reinsurance':
        data3 = pd.DataFrame(list(zip(line_data1["bulan"], line_data1["RE_pendapatan_premi"], line_data2["RE_klaim_terbayar"])),
                             columns=["bulan", "Premi Bruto", "Klaim Bruto"])
        data3_melted = pd.melt(data3, id_vars=['bulan'], var_name='Legend', value_name='in Millions Rupiah')
        data3_melted["bulan_covid"] = [pd.to_datetime("2020-03-01") for i in range(len(data3_melted))]
        data = data3_melted
        posisi = -220
    elif choose == 'Social Insurance':
        data4 = pd.DataFrame(list(zip(line_data1["bulan"], line_data1["SI_pendapatan_premi"], line_data2["SI_klaim_terbayar"])),
                             columns=["bulan", "Premi Bruto", "Klaim Bruto"])
        data4_melted = pd.melt(data4, id_vars=['bulan'], var_name='Legend', value_name='in Millions Rupiah')
        data4_melted["bulan_covid"] = [pd.to_datetime("2020-03-01") for i in range(len(data4_melted))]
        data = data4_melted
        posisi = -220
    elif choose == 'Mandatory Insurance':
        data5 = pd.DataFrame(list(zip(line_data1["bulan"], line_data1["MI_pendapatan_premi"], line_data2["MI_klaim_terbayar"])),
                             columns=["bulan", "Premi Bruto", "Klaim Bruto"])
        data5_melted = pd.melt(data5, id_vars=['bulan'], var_name='Legend', value_name='in Millions Rupiah')
        data5_melted["bulan_covid"] = [pd.to_datetime("2020-03-01") for i in range(len(data5_melted))]
        data = data5_melted
        posisi = -215
    elif choose == 'Total':
        data6 = pd.DataFrame(list(zip(line_data1["bulan"], line_data1["Total_premi"], line_data2["Total_klaim"])),
                             columns=["bulan", "Premi Bruto", "Klaim Bruto"])
        data6_melted = pd.melt(data6, id_vars=['bulan'], var_name='Legend', value_name='in Millions Rupiah')
        data6_melted["bulan_covid"] = [pd.to_datetime("2020-03-01") for i in range(len(data6_melted))]
        data = data6_melted
        posisi = -215
    chart = get_chart(data)
    ANNOTATIONS = [
        ("Mar 2020", "Awal Pandemi Covid-19"),
    ]
    annotations_df = pd.DataFrame(ANNOTATIONS, columns=["date", "event"])
    annotations_df.date = pd.to_datetime(annotations_df.date)
    annotations_df["y"] = 10
    annotation_layer = (
        alt.Chart(annotations_df)
        .mark_text(size=25, text="👇🏼", dx=-20, dy=posisi, align="left")
        .encode(
            x="date:T",
            y=alt.Y("y:Q"),
            tooltip=["event"],
        )
        .interactive()
    )
    st.altair_chart(
        (chart + annotation_layer).interactive(),
        use_container_width=True)
    st.write('')

    def get_chart3(data,color):
        hover = alt.selection_single(
            fields=["bulan"],
            nearest=True,
            on="mouseover",
            empty="none",
        )
        lines = (
            alt.Chart(data)
            .mark_line()
            .encode(
                x="bulan",
                y=alt.Y("in Millions Rupiah", title='Insurance Float (in Millions Rupiah)'),
                color=alt.value(color),
            )
        )
        points = lines.transform_filter(hover).mark_circle(size=65)
        tooltips = (
            alt.Chart(data)
            .mark_rule()
            .encode(
                x="bulan",
                y="in Millions Rupiah",
                opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
                tooltip=[
                    alt.Tooltip("bulan", timeUnit="yearmonth", title="Bulan"),
                    alt.Tooltip("in Millions Rupiah", title="Float"),
                ],
            )
            .add_selection(hover)
        )
        rule = alt.Chart(data).mark_rule(strokeDash=[5, 6], size=2).encode(
            y='average(in Millions Rupiah)',
            size=alt.value(2),
            color=alt.value("#6b6e70"),
        )
        ba = alt.Chart(data).mark_rule().encode(
            y=alt.Y('ba'),
            size=alt.value(1),
            color=alt.value("#6b6e70"),
        )
        bb = alt.Chart(data).mark_rule().encode(
            y=alt.Y('bb'),
            size=alt.value(1),
            color=alt.value("#6b6e70"),
        )
        xrule = alt.Chart(data).mark_rule().encode(
            x=alt.Y('bulan_covid', title="Bulan"),
            size=alt.value(1),
            color=alt.value("#f69697"),
        )
        return (lines + points + tooltips + rule + ba + bb + xrule).interactive()

    #control chart
    st.markdown("<h2 style='text-align: center; '>Control Chart Insurance Float</h2>", unsafe_allow_html=True)
    line_data3 = float.copy()
    line_data3["bulan"] = pd.to_datetime(line_data3["bulan"])
    line_data3['LI_avg'] = [line_data3["LI_float"].mean() for i in range(len(line_data3))]
    line_data3['GI_avg'] = [line_data3["GI_float"].mean() for i in range(len(line_data3))]
    line_data3['RE_avg'] = [line_data3["RE_float"].mean() for i in range(len(line_data3))]
    line_data3['SI_avg'] = [line_data3["SI_float"].mean() for i in range(len(line_data3))]
    line_data3['MI_avg'] = [line_data3["MI_float"].mean() for i in range(len(line_data3))]
    line_data3['Total_avg'] = [line_data3["Total_float"].mean() for i in range(len(line_data3))]

    data1 = pd.DataFrame(list(zip(line_data3["bulan"],line_data3["LI_float"])), columns=["bulan","LI_float"])
    data1["ba"] = [data1["LI_float"].mean()+(3/(len(data1)**(1/2)))*(data1["LI_float"].max()-data1["LI_float"].min()) for i in range(len(data1))]
    data1["bb"] = [data1["LI_float"].mean()-(3/(len(data1)**(1/2)))*(data1["LI_float"].max()-data1["LI_float"].min()) for i in range(len(data1))]
    data1["bulan_covid"] = [pd.to_datetime("2020-03-01") for i in range(len(data1))]
    data2 = pd.DataFrame(list(zip(line_data3["bulan"],line_data3["GI_float"])), columns=["bulan","GI_float"])
    data2["ba"] = [data2["GI_float"].mean()+(3/(len(data2)**(1/2)))*(data2["GI_float"].max()-data2["GI_float"].min()) for i in range(len(data2))]
    data2["bb"] = [data2["GI_float"].mean()-(3/(len(data2)**(1/2)))*(data2["GI_float"].max()-data2["GI_float"].min()) for i in range(len(data2))]
    data2["bulan_covid"] = [pd.to_datetime("2020-03-01") for i in range(len(data1))]
    data3 = pd.DataFrame(list(zip(line_data3["bulan"],line_data3["RE_float"])), columns=["bulan","RE_float"])
    data3["ba"] = [data3["RE_float"].mean()+(3/(len(data3)**(1/2)))*(data3["RE_float"].max()-data3["RE_float"].min()) for i in range(len(data3))]
    data3["bb"] = [data3["RE_float"].mean()-(3/(len(data3)**(1/2)))*(data3["RE_float"].max()-data3["RE_float"].min()) for i in range(len(data3))]
    data3["bulan_covid"] = [pd.to_datetime("2020-03-01") for i in range(len(data1))]
    data4 = pd.DataFrame(list(zip(line_data3["bulan"],line_data3["SI_float"])), columns=["bulan","SI_float"])
    data4["ba"] = [data4["SI_float"].mean()+(3/(len(data4)**(1/2)))*(data4["SI_float"].max()-data4["SI_float"].min()) for i in range(len(data4))]
    data4["bb"] = [data4["SI_float"].mean()-(3/(len(data4)**(1/2)))*(data4["SI_float"].max()-data4["SI_float"].min()) for i in range(len(data4))]
    data4["bulan_covid"] = [pd.to_datetime("2020-03-01") for i in range(len(data1))]
    data5 = pd.DataFrame(list(zip(line_data3["bulan"],line_data3["MI_float"])), columns=["bulan","MI_float"])
    data5["ba"] = [data5["MI_float"].mean()+(3/(len(data5)**(1/2)))*(data5["MI_float"].max()-data5["MI_float"].min()) for i in range(len(data5))]
    data5["bb"] = [data5["MI_float"].mean()-(3/(len(data5)**(1/2)))*(data5["MI_float"].max()-data5["MI_float"].min()) for i in range(len(data5))]
    data5["bulan_covid"] = [pd.to_datetime("2020-03-01") for i in range(len(data1))]
    data6 = pd.DataFrame(list(zip(line_data3["bulan"],line_data3["Total_float"])), columns=["bulan","Total_float"])
    data6["ba"] = [data6["Total_float"].mean()+(3/(len(data6)**(1/2)))*(data6["Total_float"].max()-data6["Total_float"].min()) for i in range(len(data6))]
    data6["bb"] = [data6["Total_float"].mean()-(3/(len(data6)**(1/2)))*(data6["Total_float"].max()-data6["Total_float"].min()) for i in range(len(data6))]
    data6["bulan_covid"] = [pd.to_datetime("2020-03-01") for i in range(len(data1))]


    line_data3 = line_data3.rename(columns={'LI_float':'Life Insurance (in Millions Rupiah)','GI_float':'General Insurance (in Millions Rupiah)','RE_float':'Reinsurance (in Millions Rupiah)','SI_float':'Social Insurance (in Millions Rupiah)','MI_float':'Mandatory Insurance (in Millions Rupiah)','Total_float':'Total (in Millions Rupiah)'})

    if choose == 'Life Insurance':
        posisi = -150
        data1 = data1.rename(columns={'LI_float':'in Millions Rupiah'})
        data = data1
    elif choose == 'General Insurance':
        posisi = -220
        data2 = data2.rename(columns={'GI_float':'in Millions Rupiah'})
        data = data2
    elif choose == 'Reinsurance':
        posisi = -150
        data3 = data3.rename(columns={'RE_float':'in Millions Rupiah'})
        data = data3
    elif choose == 'Social Insurance':
        posisi = -180
        data4 = data4.rename(columns={'SI_float':'in Millions Rupiah'})
        data = data4
    elif choose == 'Mandatory Insurance':
        posisi = -30
        data5 = data5.rename(columns={'MI_float':'in Millions Rupiah'})
        data = data5
    elif choose == 'Total':
        posisi = -215
        data6 = data6.rename(columns={'Total_float':'in Millions Rupiah'})
        data = data6

    chart = get_chart3(data,"#2A9D8F")
    ANNOTATIONS = [
        ("Mar 2020", "Awal Pandemi Covid-19"),
    ]
    annotations_df = pd.DataFrame(ANNOTATIONS, columns=["date", "event"])
    annotations_df.date = pd.to_datetime(annotations_df.date)
    annotations_df["y"] = 10
    annotation_layer = (
        alt.Chart(annotations_df)
        .mark_text(size=25, text="👇🏼", dx=-20, dy=posisi, align="left")
        .encode(
            x="date:T",
            y=alt.Y("y:Q"),
            tooltip=["event"],
        )
        .interactive()
    )
    st.altair_chart(
        (chart + annotation_layer).interactive(),
        use_container_width=True)

    st.header("Pembahasan")
    if choose == 'Life Insurance':
        st.markdown('<div style="text-align: justify;">Dari control chart, dapat terlihat bahwa insurance float industri asuransi jiwa setelah memasuki periode pandemi covid-19 cenderung berada di antara garis rata-rata (avg) dan garis batas bawah. Karena terdapat delapan titik berturut-turut jatuh pada daerah tersebut dan terdapat satu titik yang berada di bawah garis batas bawah, maka dapat ditarik kesimpulan bahwa insurance float industri asuransi jiwa berstatus out of control (OOC). Dengan kata lain, pandemi covid-19 memberikan dampak yang signifikan terhadap kestabilan pemasukan float industri asuransi jiwa. Hal ini mungkin saja terjadi akibat kenaikan jumlah klaim asuransi yang disebabkan oleh kematian dari virus covid-19.</div>', unsafe_allow_html=True)
    elif choose == 'General Insurance':
        st.markdown('<div style="text-align: justify;">Dari control chart, terlihat bahwa dari sebelum periode pandemi, insurance float dari industri asuransi umum memang memiliki variansi yang besar, dan tidak jarang juga terdapat titik yang berada di luar batas control chart. Setelah pandemi dimulai, float tetap memiliki variansi dan pola yang cenderung sama. Oleh karena itu, dapat disimpulkan bahwa kestabilan pemasukan float industri asuransi umum tidak dipengaruhi secara signifikan oleh adanya pandemi covid-19.</div>', unsafe_allow_html=True)
    elif choose == 'Reinsurance':
        st.markdown('<div style="text-align: justify;">Dari control chart, terlihat bahwa sebelum pandemi, insurance float industri reasuransi memiliki variansi yang cenderung kecil, dimana titik-titiknya tidak tersebar jauh dari garis rata-ratanya. Setelah pandemi dimulai, terlihat peningkatan variansi dari float, dimana titik-titiknya menjadi tersebar cukup jauh dari garis rata-ratanya. Sehingga, dapat ditarik kesimpulan bahwa pandemi covid-19 memberikan pengaruh yang signifikan terhadap kestabilan pemasukan float industri reasuransi. Ini bisa saja disebabkan oleh demand asuransi dan jumlah klaim dari perusahaan asuransi yang cenderung meningkat membuat insurance float dari reasuransi menjadi lebih fluktuatif.</div>', unsafe_allow_html=True)
    elif choose == 'Social Insurance':
        st.markdown('<div style="text-align: justify;">Dari control chart, dapat terlihat bahwa sejak pandemi dimulai, semua titik insurance float industri asuransi sosial berada di atas garis rata-rata (OOC), terlihat juga bahwa kondisi insurance float sebelum pandemi malah cenderung di bawah garis rata-rata. Hal ini mengindikasikan adanya kenaikan pemasukan float yang cukup besar setelah mulainya pandemi. Oleh sebab itu, dapat disimpulkan bahwa pandemi covid-19 memberikan dampak yang signifikan terhadap kestabilan pemasukan float industri asuransi sosial. Hal ini dapat disebabkan oleh peningkatan jumlah nasabah selama pandemi karena premi dari jasa asuransi sosial cenderung lebih murah daripada jasa asuransi lainnya. Asuransi sosial pun tidak bertujuan mencari keuntungan sehingga menarik masyarakat yang ingin berasuransi saat pandemi.</div>', unsafe_allow_html=True)
    elif choose == 'Mandatory Insurance':
        st.markdown('<div style="text-align: justify;">Asuransi ASN, TNI/POLRI, Kecelakaan Penumpang Umum dan Lalu Lintas Jalan memang tidak bertujuan untuk mencari keuntungan, melainkan dibuat sebagai hak-hak yang disediakan oleh negara. Pada control chart, terlihat bahwa insurance float cenderung terus turun dari sebelum pandemi sampai setelah pandemi dimulai. Hal ini disebabkan oleh terus menaiknya jumlah klaim walaupun premi yang masuk cenderung konstan. Menurunnya insurance float setelah pandemi menembus garis batas bawah (OOC), sehingga dapat disimpulkan bahwa pandemi covid-19 memberikan dampak yang signifikan terhadap kestabilan pemasukan float mandatory insurance.</div>', unsafe_allow_html=True)
    elif choose == 'Total':
        st.markdown('<div style="text-align: justify;">Dari control chart, terlihat bahwa sebelum dan setelah memasuki periode pandemi, insurance float dari keseluruhan industri asuransi tidak mengalami perubahan variansi yang signifikan dan tidak menunjukkan adanya indikasi out of control (OOC). Sehingga, dapat disimpulkan bahwa pandemi covid-19 tidak mempengaruhi pemasukan float industri asuransi secara keseluruhan.</div>', unsafe_allow_html=True)

    st.write(" ")
    st.markdown("""---""")
    st.header("Kesimpulan dan Saran")
    st.markdown('<div style="text-align: justify;">Meskipun kestabilan pemasukan float asuransi konvensional (selain Asuransi Umum) terguncang oleh pandemi covid-19, secara keseluruhan, industri asuransi di Indonesia berhasil bertahan. Komisaris Utama Indonesia Financial Group (IFG), Fauzi Ichsan, percaya bahwa potensi pertumbuhan industri asuransi di Indonesia masih besar. Kedepannya, perusahaan asuransi perlu memperhatikan peningkatan kualitas SDM dengan pengembangan kapasitas aktuarial, mengakselerasikan IT platform, memperketat modal minimum, dan lain-lain.</div>', unsafe_allow_html=True)

elif select == "Glossary":
    st.subheader("Glossary")
    a=1
    b=4
    koloms1, koloms2 = st.columns([a,b])
    with koloms1:
        st.markdown('Asuransi (_Insurance_)')
    with koloms2:
        st.markdown('<div style="text-align: justify;">Perjanjian antara dua pihak, yaitu perusahaan asuransi dan pemegang polis, yang menjadi dasar bagi penerimaan premi oleh perusahaan asuransi sebagai imbalan untuk memberikan penggantian kepada tertanggung atau pemegang polis karena kerugian, kerusakan, biaya yang timbul, kehilangan keuntungan, atau tanggung jawab hukum kepada pihak ketiga yang mungkin diderita tertanggung atau pemegang polis karena terjadinya suatu peristiwa yang tidak pasti; atau memberikan pembayaran yang didasarkan pada meninggalnya tertanggung atau pembayaran yang didasarkan pada hidupnya tertanggung dengan manfaat yang besarnya telah ditetapkan dan/atau didasarkan pada hasil pengelolaan dana.</div>', unsafe_allow_html=True)
        st.write("")
    koloms1, koloms2 = st.columns([a, b])
    with koloms1:
        st.markdown('Premi (_Premium_)')
    with koloms2:
        st.markdown(
            '<div style="text-align: justify;">Biaya yang ditanggung dan harus dibayarkan nasabah dalam jangka waktu tertentu sesuai kesepakatan dengan pihak perusahaan asuransi.</div>',
            unsafe_allow_html=True)
        st.write("")
    koloms1, koloms2 = st.columns([a, b])
    with koloms1:
        st.markdown('Klaim (_Claim_)')
    with koloms2:
        st.markdown(
            '<div style="text-align: justify;">Tuntutan dari pihak tertanggung karena adanya kontrak perjanjian dengan pihak asuransi untuk menjamin pembayaran ganti rugi selama pembayaran premi telah dilakukan oleh pihak tertanggung.</div>',
            unsafe_allow_html=True)
        st.write("")
    koloms1, koloms2 = st.columns([a, b])
    with koloms1:
        st.markdown('_Insurance Float_')
    with koloms2:
        st.markdown(
            '<div style="text-align: justify;">Selisih antara premi yang dikumpulkan oleh perusahaan asuransi dengan klaim yang harus dibayarkan pada nasabah.</div>',
            unsafe_allow_html=True)
        st.write("")
    koloms1, koloms2 = st.columns([a,b])
    with koloms1:
        st.markdown('Asuransi Jiwa (_Life Insurance_)')
    with koloms2:
        st.markdown('<div style="text-align: justify;">Usaha yang menyelenggarakan jasa penanggulangan risiko dengan memberikan pembayaran kepada pemegang polis, tertanggung, atau pihak Lain yang berhak dalam hal tertanggung meninggal dunia atau tetap hidup, atau pembayaran lain kepada pemegang polis, tertanggung, atau pihak lain yang berhak pada waktu tertentu yang diatur dalam perjanjian, yang besarnya telah ditetapkan dan/atau didasarkan pada hasil pengelolaan dana.</div>', unsafe_allow_html=True)
        st.write("")
    koloms1, koloms2 = st.columns([a,b])
    with koloms1:
        st.write("")
        st.markdown('Asuransi Umum (_General Insurance_)')
    with koloms2:
        st.markdown('<div style="text-align: justify;">Usaha jasa pertanggungan risiko yang memberikan penggantian kepada tertanggung atau pemegang polis karena kerugian, kerusakan, biaya yang timbul, kehilangan keuntungan, atau tanggung jawab hukum kepada pihak ketiga yang mungkin diderita tertanggung atau pemegang polis karena terjadinya suatu peristiwa yang tidak pasti.</div>', unsafe_allow_html=True)
        st.write("")
    koloms1, koloms2 = st.columns([a,b])
    with koloms1:
        st.markdown('Reasuransi (_Reinsurance_)')
    with koloms2:
        st.markdown('<div style="text-align: justify;">Usaha jasa pertanggungan ulang terhadap risiko yang dihadapi oleh perusahaan asuransi, perusahaan penjaminan, atau perusahaan reasuransi lainnya.</div>', unsafe_allow_html=True)
        st.write("")
    koloms1, koloms2 = st.columns([a,b])
    with koloms1:
        st.write("")
        st.markdown('Asuransi Sosial (_Social Insurance_)')
    with koloms2:
        st.markdown('<div style="text-align: justify;">Asuransi yang menyediakan jaminan sosial bagi anggota masyarakat yang dibentuk oleh pemerintah bedasarkan peraturan-peraturan yang mengatur hubungan antara pihak asuransi dengan seluruh golongan masyarakat.</div>', unsafe_allow_html=True)
        st.write("")
    koloms1, koloms2 = st.columns([a,b])
    with koloms1:
        st.markdown('Asuransi ASN, TNI/POLRI, Kecelakaan Penumpang Umum dan Lalu Lintas Jalan (_Mandatory Insurance_)')
    with koloms2:
        st.markdown('<div style="text-align: justify;">Merupakan program asuransi yang dijalankan oleh PT. ASABRI (Persero), PT. Taspen (Persero) dan PT. Jasa Raharja (Persero)</div>', unsafe_allow_html=True)
        st.write("")

elif select == "Links":
    st.subheader("Data Sources")
    st.write("OJK: https://www.ojk.go.id/id/kanal/iknb/data-dan-statistik/asuransi/")
    st.write("DataIndonesia.id: https://dataindonesia.id/bursa-keuangan/detail/jumlah-perusahaan-asuransi-indonesia-capai-149-unit-pada-2021")
    st.write("")
    st.subheader("References")
    st.markdown("_Bagaimana Perusahaan asuransi Mendapat Uang? Ini Penjelasannya!_ Simulasi Kredit. (n.d.). Retrieved July 27, 2022, from https://www.simulasikredit.com/bagaimana-perusahaan-asuransi-mendapat-uang-ini-penjelasannya/ ")
    st.markdown("_Menilik Dampak Pandemi Pada industri asuransi dan prospeknya._ Indonesia Financial Group. (2021, June 3). Retrieved August 27, 2022, from https://ifg.id/id/blog/menilik-dampak-pandemi-pada-industri-asuransi-dan-prospeknya ")
    st.markdown("Walpole, R. E., & Myers, R. H. (1985). _Probability and statistics for engineers and scientists._ New York: Macmillan.")
    st.write("")

    st.subheader("Download Cleaned Data")
    def convert_df(df):
        return df.to_csv().encode('utf-8')
    csv_1 = convert_df(premi)
    csv_2 = convert_df(klaim)
    csv_3 = convert_df(perusahaan)
    st.download_button(
        label="pendapatan_premi.csv",
        data=csv_1,
        file_name='pendapatan_premi.csv',
        mime='text/csv',
    )
    st.download_button(
        label="klaim_terbayar.csv",
        data=csv_2,
        file_name='klaim_terbayar.csv',
        mime='text/csv',
    )
    st.download_button(
        label="perusahaan_asuransi.csv",
        data=csv_3,
        file_name='perusahaan_asuransi.csv',
        mime='text/csv',
    )
