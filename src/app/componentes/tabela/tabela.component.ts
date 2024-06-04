import { CommonModule } from '@angular/common';
import { Component, ElementRef } from '@angular/core';
import { PortfolioService } from '../../service/portfolioService/portfolio.service';
import { Portfolio } from '../../interface/portfolio';
import { FormsModule } from '@angular/forms';
import {
  MatSnackBar,
  MatSnackBarHorizontalPosition,
  MatSnackBarVerticalPosition,
} from '@angular/material/snack-bar';
import { MatButtonModule } from '@angular/material/button';
import { MatSelectModule } from '@angular/material/select';
import { MatFormFieldModule } from '@angular/material/form-field';
import { Router } from '@angular/router';
import { FinanceYahooServiceService } from '../../service/financeYahooService/finance-yahoo-service.service';



@Component({
  selector: 'app-tabela',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    MatFormFieldModule,
    MatSelectModule,
    MatButtonModule,
  ],
  templateUrl: './tabela.component.html',
  styleUrl: './tabela.component.css',
})
export class TabelaComponent {

  portfolio: Portfolio[] = []
  valorTotalCarteira: number = 0
  metaTotalCarteira: number = 0
  valorTotalAporte: number = 0

  constructor(
    private _PortfolioService: PortfolioService,
    private _snackBar: MatSnackBar,
    private _Router: Router,
    private _FinanceYahooServiceService: FinanceYahooServiceService
  ) { }

  ngOnInit(): void {
    //Init
    this.listarCarteira()

  }

  listarCarteira(): void {
    //Listar carteira
    this._PortfolioService.listarCarteira().subscribe((response) => {
      this.portfolio = response
      this.portfolio.forEach((data) => { data.valor = data.cotacao * data.quantidade })
      this.atualizarValorTotalCarteira() //Atualizando o valor total da carteira
      this.atualizarMetaTotal() //Atualizar o valor total da meta
    })
  }

  atualizarValorTotalCarteira(): void {
    //Maneira de somar valores totais
    this.valorTotalCarteira = this.portfolio.reduce((accumulator, currentValue) => accumulator + currentValue.valor, 0)
  }

  atualizarMeta(event: any, id: any): void {
    //Atualizar meta
    let ativo: any
    this._PortfolioService.getAtivo(id).subscribe((response) => {
      ativo = response
      ativo.meta = parseFloat(event.target.value)
      this._PortfolioService.atualizarAtivo(id, ativo).subscribe()
      this.openSnackBar(`${ativo.ativo} - Meta atualizada !!!`)
      this.atualizarMetaTotal()
    })
  }

  atualizarMetaTotal(): void {
    //Funcao de soma de meta total
    this._PortfolioService.listarCarteira().subscribe((response) => {
      this.metaTotalCarteira = response.reduce((accumulator, currentValue) => accumulator + currentValue.meta, 0)
    })
  }

  atualizarStatus(event: any, id: any): void {
    //Atualizar status
    let ativo: any
    this._PortfolioService.getAtivo(id).subscribe((response) => {
      ativo = response
      if (event.target.value == 1) {
        ativo.status = 'comprar';
      } if (event.target.value == 2) {
        ativo.status = 'aguardar'
      } if (event.target.value == 3) {
        ativo.status = 'vender'
      }

      this._PortfolioService.atualizarAtivo(id, ativo).subscribe()
      this.openSnackBar(`${ativo.ativo} - Status atualizado !!!`)

    })
  }

  atualizarComentario(event: any, id: any): void {
    //Atualizar comentario
    let ativo: any
    this._PortfolioService.getAtivo(id).subscribe((response) => {
      ativo = response
      ativo.comentarios = event.target.value
      this._PortfolioService.atualizarAtivo(id, ativo).subscribe()
      this.openSnackBar(`${ativo.ativo} - Comentario atualizado !!!`)
    })
  }

  // Mensagem Box
  horizontalPosition: MatSnackBarHorizontalPosition = 'end';
  verticalPosition: MatSnackBarVerticalPosition = 'bottom';
  durationInSeconds = 5;
  openSnackBar(mensagem: string) {
    this._snackBar.open(mensagem, 'Close', {
      horizontalPosition: this.horizontalPosition,
      verticalPosition: this.verticalPosition,
      duration: this.durationInSeconds * 1000,

    });
  }

  calculoCotas(id: any, event: any): void {
    //Calculo Cotas e aporte
    this.portfolio.filter((x) => {
      if (x.id == id) {
        x.valor = (x.cotacao * (x.quantidade + parseInt(event.target.value)))
        x.aporte = x.cotacao * parseInt(event.target.value)

        //Calcular o valor total do aporte
        this.valorTotalAporte = this.portfolio.reduce((accumulator, currentValue) => accumulator + currentValue.aporte, 0)
        this.atualizarValorTotalCarteira()

      }
    })

  }

  TermSearch:string = ""
  searchTerm(TermSearch:string): void {
    this._PortfolioService.search(this.TermSearch).subscribe((data)=>{
      this.portfolio = data
    })
  }

}
