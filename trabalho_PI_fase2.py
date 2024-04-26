import tabulate as tabulate 
import pandas as pd 
from colorama import init, Fore, Back, Style
import oracledb
import getpass

A=int(input("Digite 1 para inserir, 2 para listar, 3 para atualizar ou 4 para deletar: "))
#conexão com o oracle
userpwd = getpass.getpass("Enter password: ")
connection = oracledb.connect(user="PEDRO", password=userpwd,
                              host="localhost", port=1521, service_name="XEPDB1")
cursor = connection.cursor()

  #inserir um produto
if(A==1):
  # todas as variaves do cadastro de produto
    Cp = int(input("Informe o código do produto: "))
    Np = str(input("Informe o nome do produto: "))
    Dp = str(input("Informe a descrição do produto: "))
    Ca = float(input("Informe o custo do produto: "))
    Cf = float(input("Informe o custo fixo: "))
    Cv = float(input("Informe o quanto será a comissão de vendas: "))
    Iv = float(input("Informe os impostos: "))
    Ml = float(input("Informe a rentabilidade: "))



    #calculo do preço de venda  
    soma=Cf+Cv+Iv+Ml
    if(soma>100):
      soma=soma*-1


    if soma != 100:
      Pv = Ca / (1 - (soma / 100))
    else:
      Pv = Ca /1

    if(Ml>100):
      soma=soma*-1

    
    if (Pv<0):
      Pv=Pv*(-1)
    print(f"{Pv}")
    Rb = Pv - Ca

    custoAq = Ca
    pca=Ca/Pv*100
    receitaBruta = Pv-Ca
    Prb=receitaBruta/Pv*100
    impostos = (Iv/100) * Pv
    comissãoVendas =(Cv/100) * Pv
    rentabilidade = (Ml/100) * Pv
    outrosCustos = Cf+Cv+Iv
    outrosCustos1 = (Cf + Cv + Iv)/(100) * Pv 
    custoFixo = (Cf/100) * Pv


    #tabela da inserção
    tabela = {
        "Descrição": ["A-Preço de venda", "B-Custo de aquisação(fornecedor)", "C-Receita Bruta(A-B)","D-Custo fixo/administrativo","E-Comissão de vendas", "F-Impostos", "G-Rentabilidade", "F-Outros Custos"],
        "Valor": [Pv,custoAq,receitaBruta,custoFixo,comissãoVendas,impostos,rentabilidade,outrosCustos1],
        "%": ["100%", (f"{pca}%"), (f"{Prb}%"),(f"{Cf}%"),(f"{Cv}%"), (f"{Iv}%"), (f"{Ml}%"), (f"{outrosCustos}%")]
    }

    print(tabulate.tabulate(tabela, headers='keys', tablefmt='fancy_grid'))

    #analise de faixa de lucro 

    if Ml > 20:
      nomeTab = "O lucro será Alto"
    elif Ml> 10 and Ml <= 20:
      nomeTab = "O lucro será Médio"
    elif Ml > 0 and Ml <= 10:
      nomeTab = "O lucro será Baixo"
    elif Ml == 0:
      nomeTab = "Não irá ter lucro nem prejuizo (equilíbrio)"
    elif Ml < 0:  
      nomeTab = "Prejuizo"
    
    lucro = Ml

    #tabela de lucro
    tabLuc = {
    "Resultado": [f"{lucro}%", f"{nomeTab}"]
    }
    print(tabulate.tabulate(tabLuc, headers='keys', tablefmt="fancy_grid"))

    #inserção no banco de dados
    data=[(Cp,Np,Dp,Ca,Cf,Cv,Iv,Ml)]
    cursor.executemany("insert into PRODUTOS (cod_prod, nome_prod, desc_prod, custo_prod, custo_fixo, comissao_vendas, imposto, margem_lucro) values (:1, :2, :3, :4, :5, :6, :7, :8)",data)
    connection.commit()                                                    





  #listagem de produto
elif (A == 2):
    #tabela com todos os produtos
    cursor = connection.cursor()
    cursor.execute("select * from PRODUTOS")
    rows = cursor.fetchall()

    headers = ["Código", "Nome", "Descrição", "Custo", "Custo Fixo", "Comissão Vendas", "Imposto", "Rentabilidade"]
    dados_produtos = [[row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]] for row in rows]

    print(tabulate.tabulate(dados_produtos, headers=headers, tablefmt='fancy_grid'))
    
    #tabela com cada produto
    cursor.execute("SELECT * FROM PRODUTOS")
    rows = cursor.fetchall()

    for row in rows:
        soma = row[4] + row[5] + row[6] + row[7]
        if(soma>100):
            soma=soma*-1


        if soma != 100:
            Pv = row[3] / (1 - (soma / 100))
        else:
            Pv = row[3] /1
        if row[7] > 100:
            soma = soma * -1

        custoAq = row[3]
        pca = custoAq / Pv * 100
        receitaBruta = Pv - custoAq
        Prb = receitaBruta / Pv * 100
        impostos = row[6] / 100 * Pv
        comissãoVendas = row[5] / 100 * Pv
        rentabilidade = row[7] / 100 * Pv
        outrosCustos = row[4] + row[5] + row[6]
        outrosCustos1 = outrosCustos / 100 * Pv
        custoFixo = row[4] / 100 * Pv
        
        #calculo lucro
        lucro=row[7]
        if row[7] > 20:
          nomeTab = "O lucro será Alto"
        elif row[7]> 10 and row[7] <= 20:
          nomeTab = "O lucro será Médio"
        elif row[7] > 0 and row[7] <= 10:
          nomeTab = "O lucro será Baixo"
        elif row[7] == 0:
          nomeTab = "Não irá ter lucro nem prejuizo (equilíbrio)"
        elif row[7] < 0:  
          nomeTab = "Prejuizo"

        tabela1 = {
            "tabela2": ["Código", "Nome", "Descrição", "Custo", "Custo Fixo", "Comissão Vendas", "Imposto", "Rentabilidade"],
            "dados_tabela": [[row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]]],
        }
        tabela_porcentagem = [
            ["Soma","Pv","Ca","Pca","Rb","Prb","Iv","Cv","Renta","Oc","Oc1","Cf"],
            [(f"{soma:,.2f}"), (f"{Pv:,.2f}"), (f"{custoAq:,.2f}"), (f"{pca:,.2f}"), (f"{receitaBruta:,.2f}"), (f"{Prb:,.2f}"), (f"{impostos:,.2f}"), (f"{comissãoVendas:,.2f}"), (f"{rentabilidade:,.2f}"), 
             (f"{outrosCustos:,.2f}"), (f"{outrosCustos1:,.2f}"), (f"{custoFixo:,.2f}")]
        ]
        tabela2 = {
        "Descrição": ["A-Preço de venda", "B-Custo de aquisação(fornecedor)", "C-Receita Bruta(A-B)","D-Custo fixo/administrativo","E-Comissão de vendas", "F-Impostos", "G-Rentabilidade", "F-Outros Custos"],
        "Valor": [(f"{Pv:,.2f}"),(f"{custoAq:,.2f}"),(f"{receitaBruta:,.2f}"),(f"{custoFixo:,.2f}"),(f"{comissãoVendas:,.2f}"),(f"{impostos:,.2f}"),(f"{rentabilidade:,.2f}"),(f"{outrosCustos1:,.2f}")],
        "%": ["100%", (f"{pca:,.2f}%"), (f"{Prb:,.2f}%"),(f"{ row[4]}%"),(f"{ row[5]}%"), (f"{ row[6]}%"), (f"{ row[7]}%"), (f"{outrosCustos}%")]
    }
        tabLuc = {
          "Resultado": [f"{lucro}%", f"{nomeTab}"]
                }
        
        print("Dados do Produto:")
        print(tabulate.tabulate(tabela1['dados_tabela'], headers=tabela1['tabela2'], tablefmt='fancy_grid'))
        print("Tabela de Porcentagem:")
        print(tabulate.tabulate(tabela2, tablefmt='fancy_grid'))
        print(tabulate.tabulate(tabLuc, headers='keys', tablefmt="fancy_grid"))
        print("\nOutros Dados:")
        for key, value in tabela1.items():
            if key not in ['tabela2', 'dados_tabela', 'tabela_porcentagem']:
                print(f"{key}: {value}")
        print()

   
  #atualização de produtos
elif(A==3):
      
      Cp = int(input("Informe o código do produto a ser atualizado: "))
      Np = str(input("Informe o novo nome do produto: "))
      Dp = str(input("Informe a nova descrição do produto: "))
      Ca = float(input("Informe o novo custo do produto: "))
      Cf = float(input("Informe o novo custo fixo: "))
      Cv = float(input("Informe o quanto será a nova comissão de vendas: "))
      Iv = float(input("Informe os impostos: "))
      Ml = float(input("Informe a nova rentabilidade: "))


  #deletar produtos
elif(A==4):
    cursor = connection.cursor()
    cursor.execute("select * from PRODUTOS")
    rows = cursor.fetchall()
    for row in rows:
      print(row)
    Cpd=int(input("Digite o código do produto que deseja deletar:"))
    delete="DELETE FROM PRODUTOS WHERE cod_prod= :Cpd"
    cursor.execute(delete, Cpd=Cpd)
    connection.commit()
    print(f"Produto deletado com sucesso")


cursor.close()
connection.close()