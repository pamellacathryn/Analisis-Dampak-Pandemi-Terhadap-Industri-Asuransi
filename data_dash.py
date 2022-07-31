import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
from streamlit_option_menu import option_menu

# dataset
perusahaan = pd.read_csv('perusahaan.csv')
premi = pd.read_csv('pendapatan_premi.csv')
klaim = pd.read_csv('klaim_terbayar.csv')
float_1 = pd.merge(premi, klaim, how='left', on='bulan')
float = pd.DataFrame(list(zip(
    float_1["bulan"],
    float_1["LI_pendapatan_premi"]-float_1["LI_klaim_terbayar"],
    float_1["GI_pendapatan_premi"]-float_1["GI_klaim_terbayar"],
    float_1["RE_pendapatan_premi"]-float_1["RE_klaim_terbayar"],
    float_1["SI_pendapatan_premi"]-float_1["SI_klaim_terbayar"],
    float_1["MI_pendapatan_premi"]-float_1["MI_klaim_terbayar"]
)), columns = ["bulan","LI_float","GI_float","RE_float","SI_float","MI_float"])

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
    st.markdown("<h6 style='text-align: center; '>Pamella Cathryn - DQLab Tetris Program Batch II</h6>",
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
    def get_chart(data,x,color,judul,comment,ylabel):
        a = data.columns[x]
        hover = alt.selection_single(
            fields=["bulan"],
            nearest=True,
            on="mouseover",
            empty="none",
        )
        lines = (
            alt.Chart(data, title=judul)
            .mark_line()
            .encode(
                x="bulan",
                y=alt.Y(a, title=ylabel),
                color=alt.value(color),
            )
        )
        points = lines.transform_filter(hover).mark_circle(size=65)
        tooltips = (
            alt.Chart(data)
            .mark_rule()
            .encode(
                x="bulan",
                y=a,
                opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
                tooltip=[
                    alt.Tooltip("bulan", timeUnit="yearmonth", title="Bulan"),
                    alt.Tooltip(a, title=comment),
                ],
            )
            .add_selection(hover)
        )
        xrule = alt.Chart(data).mark_rule().encode(
            x=alt.Y('bulan_covid', title="bulan"),
            size=alt.value(1),
            color=alt.value("#f69697"),
        )
        return (lines + points + tooltips + xrule).interactive()

    choose = st.selectbox(
            'Jenis Asuransi:',
            ('Life Insurance', 'General Insurance', 'Reinsurance', 'Social Insurance', 'Mandatory Insurance'))
    st.write("")
    #line chart premi
    st.markdown("<h4 style='text-align: center; '>Perkembangan Pendapatan Premi 2016-2021</h4>", unsafe_allow_html=True)
    line_data1 = premi.copy()
    line_data1["bulan"] = pd.to_datetime(line_data1["bulan"])
    line_data1["bulan_covid"] = [pd.to_datetime("2020-03-01") for i in range(len(line_data1))]
    line_data1 = line_data1.rename(columns={'LI_pendapatan_premi':'Life Insurance (in Millions Rupiah)','GI_pendapatan_premi':'General Insurance (in Millions Rupiah)','RE_pendapatan_premi':'Reinsurance (in Millions Rupiah)','SI_pendapatan_premi':'Social Insurance (in Millions Rupiah)','MI_pendapatan_premi':'Mandatory Insurance (in Millions Rupiah)'})
    if choose == 'Life Insurance':
        posisi = -220
        p = 1
        color = '#457b9d'
    elif choose == 'General Insurance':
        posisi = -220
        p = 2
        color = '#2A9D8F'
    elif choose == 'Reinsurance':
        posisi = -220
        p = 3
        color = '#E9C46A'
    elif choose == 'Social Insurance':
        posisi = -220
        p = 4
        color = '#F4A261'
    elif choose == 'Mandatory Insurance':
        posisi = -215
        p = 5
        color = '#E76F51'
    chart = get_chart(line_data1,p,color,"","Premi Bruto",'Premi Bruto (in Millions Rupiah)')
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

    #line chart klaim
    st.markdown("<h4 style='text-align: center; '>Perkembangan Klaim Dibayar 2016-2021</h4>", unsafe_allow_html=True)
    line_data2 = klaim.copy()
    line_data2["bulan"] = pd.to_datetime(line_data2["bulan"])
    line_data2["bulan_covid"] = [pd.to_datetime("2020-03-01") for i in range(len(line_data2))]
    line_data2 = line_data2.rename(columns={'LI_klaim_terbayar':'Life Insurance (in Millions Rupiah)','GI_klaim_terbayar':'General Insurance (in Millions Rupiah)','RE_klaim_terbayar':'Reinsurance (in Millions Rupiah)','SI_klaim_terbayar':'Social Insurance (in Millions Rupiah)','MI_klaim_terbayar':'Mandatory Insurance (in Millions Rupiah)'})
    if choose == 'Life Insurance':
        posisi = -215
        p = 1
        color = '#457b9d'
    elif choose == 'General Insurance':
        posisi = -220
        p = 2
        color = '#2A9D8F'
    elif choose == 'Reinsurance':
        posisi = -215
        p = 3
        color = '#E9C46A'
    elif choose == 'Social Insurance':
        posisi = -215
        p = 4
        color = '#F4A261'
    elif choose == 'Mandatory Insurance':
        posisi = -215
        p = 5
        color = '#E76F51'
    chart = get_chart(line_data2,p,color,"","Klaim Bruto",'Klaim Bruto (in Millions Rupiah)')
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
            x=alt.Y('bulan_covid', title="bulan"),
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

    line_data3 = line_data3.rename(columns={'LI_float':'Life Insurance (in Millions Rupiah)','GI_float':'General Insurance (in Millions Rupiah)','RE_float':'Reinsurance (in Millions Rupiah)','SI_float':'Social Insurance (in Millions Rupiah)','MI_float':'Mandatory Insurance (in Millions Rupiah)'})

    if choose == 'Life Insurance':
        posisi = -150
        data1 = data1.rename(columns={'LI_float':'in Millions Rupiah'})
        data = data1
        color = '#457b9d'
    elif choose == 'General Insurance':
        posisi = -220
        data2 = data2.rename(columns={'GI_float':'in Millions Rupiah'})
        data = data2
        color = '#2A9D8F'
    elif choose == 'Reinsurance':
        posisi = -150
        data3 = data3.rename(columns={'RE_float':'in Millions Rupiah'})
        data = data3
        color = '#E9C46A'
    elif choose == 'Social Insurance':
        posisi = -180
        data4 = data4.rename(columns={'SI_float':'in Millions Rupiah'})
        data = data4
        color = '#F4A261'
    elif choose == 'Mandatory Insurance':
        posisi = -30
        data5 = data5.rename(columns={'MI_float':'in Millions Rupiah'})
        data = data5
        color = '#E76F51'

    chart = get_chart3(data,color)
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

    st.header("Kesimpulan")
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

elif select == "Glossary":
    st.subheader("Glossary")
    a=1
    b=4
    koloms1, koloms2 = st.columns([a,b])
    with koloms1:
        st.write("Asuransi")
    with koloms2:
        st.markdown('<div style="text-align: justify;">Perjanjian antara dua pihak, yaitu perusahaan asuransi dan pemegang polis, yang menjadi dasar bagi penerimaan premi oleh perusahaan asuransi sebagai imbalan untuk memberikan penggantian kepada tertanggung atau pemegang polis karena kerugian, kerusakan, biaya yang timbul, kehilangan keuntungan, atau tanggung jawab hukum kepada pihak ketiga yang mungkin diderita tertanggung atau pemegang polis karena terjadinya suatu peristiwa yang tidak pasti; atau memberikan pembayaran yang didasarkan pada meninggalnya tertanggung atau pembayaran yang didasarkan pada hidupnya tertanggung dengan manfaat yang besarnya telah ditetapkan dan/atau didasarkan pada hasil pengelolaan dana.</div>', unsafe_allow_html=True)
        st.write("")
    koloms1, koloms2 = st.columns([a, b])
    with koloms1:
        st.write("Premi")
    with koloms2:
        st.markdown(
            '<div style="text-align: justify;">Biaya yang ditanggung dan harus dibayarkan nasabah dalam jangka waktu tertentu sesuai kesepakatan dengan pihak perusahaan asuransi.</div>',
            unsafe_allow_html=True)
        st.write("")
    koloms1, koloms2 = st.columns([a, b])
    with koloms1:
        st.write("Klaim")
    with koloms2:
        st.markdown(
            '<div style="text-align: justify;">Tuntutan dari pihak tertanggung karena adanya kontrak perjanjian dengan pihak asuransi untuk menjamin pembayaran ganti rugi selama pembayaran premi telah dilakukan oleh pihak tertanggung.</div>',
            unsafe_allow_html=True)
        st.write("")
    koloms1, koloms2 = st.columns([a, b])
    with koloms1:
        st.write("Insurance Float")
    with koloms2:
        st.markdown(
            '<div style="text-align: justify;">Selisih antara premi yang dikumpulkan oleh perusahaan asuransi dengan klaim yang harus dibayarkan pada nasabah.</div>',
            unsafe_allow_html=True)
        st.write("")
    koloms1, koloms2 = st.columns([a,b])
    with koloms1:
        st.write("Asuransi Jiwa")
    with koloms2:
        st.markdown('<div style="text-align: justify;">Usaha yang menyelenggarakan jasa penanggulangan risiko dengan memberikan pembayaran kepada pemegang polis, tertanggung, atau pihak Lain yang berhak dalam hal tertanggung meninggal dunia atau tetap hidup, atau pembayaran lain kepada pemegang polis, tertanggung, atau pihak lain yang berhak pada waktu tertentu yang diatur dalam perjanjian, yang besarnya telah ditetapkan dan/atau didasarkan pada hasil pengelolaan dana.</div>', unsafe_allow_html=True)
        st.write("")
    koloms1, koloms2 = st.columns([a,b])
    with koloms1:
        st.write("Asuransi Umum")
    with koloms2:
        st.markdown('<div style="text-align: justify;">Usaha jasa pertanggungan risiko yang memberikan penggantian kepada tertanggung atau pemegang polis karena kerugian, kerusakan, biaya yang timbul, kehilangan keuntungan, atau tanggung jawab hukum kepada pihak ketiga yang mungkin diderita tertanggung atau pemegang polis karena terjadinya suatu peristiwa yang tidak pasti.</div>', unsafe_allow_html=True)
        st.write("")
    koloms1, koloms2 = st.columns([a,b])
    with koloms1:
        st.write("Reasuransi")
    with koloms2:
        st.markdown('<div style="text-align: justify;">Usaha jasa pertanggungan ulang terhadap risiko yang dihadapi oleh perusahaan asuransi, perusahaan penjaminan, atau perusahaan reasuransi lainnya.</div>', unsafe_allow_html=True)
        st.write("")
    koloms1, koloms2 = st.columns([a,b])
    with koloms1:
        st.write("Asuransi Sosial")
    with koloms2:
        st.markdown('<div style="text-align: justify;">Asuransi yang menyediakan jaminan sosial bagi anggota masyarakat yang dibentuk oleh pemerintah bedasarkan peraturan-peraturan yang mengatur hubungan antara pihak asuransi dengan seluruh golongan masyarakat.</div>', unsafe_allow_html=True)
        st.write("")
    koloms1, koloms2 = st.columns([a,b])
    with koloms1:
        st.write("Asuransi ASN, TNI/POLRI, Kecelakaan Penumpang Umum dan Lalu Lintas Jalan")
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
