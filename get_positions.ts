import { readFileSync } from "fs";
import { Keypair,PublicKey} from "@solana/web3.js";
import { TOKEN_PROGRAM_ID } from '@solana/spl-token'
import {
    WhirlpoolContext, buildWhirlpoolClient, ORCA_WHIRLPOOL_PROGRAM_ID,
    PDAUtil, PriceMath,AccountFetcher, PoolUtil
  } from "@orca-so/whirlpools-sdk";
import { DecimalUtil} from "@orca-so/common-sdk";
import { AnchorProvider } from "@project-serum/anchor";

const token_map: { [key: string]: number } = {
  "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v": 1,
  "So11111111111111111111111111111111111111112": 0,
  "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263": 2,
};

const main = async() => {
    const secretKeyString = readFileSync("lp.json",{encoding:'utf8'});
    const secretKey = Uint8Array.from(JSON.parse(secretKeyString));
    const owner = Keypair.fromSecretKey(secretKey);
    //console.log(owner);
    const provider = AnchorProvider.env();
    const ctx = WhirlpoolContext.withProvider(provider, ORCA_WHIRLPOOL_PROGRAM_ID);
    const fetcher = new AccountFetcher(ctx.provider.connection);
    const client = buildWhirlpoolClient(ctx);
    const connection = provider.connection;
    const atas = await connection.getParsedTokenAccountsByOwner(provider.wallet.publicKey,{programId: TOKEN_PROGRAM_ID})

    const sleep = async (milliseconds:number) => {
      return new Promise(resolve => setTimeout(resolve, milliseconds))
    }
    
    let final_res = [0.0,0.0,0.0,0];
    var num:number = 0 ; 
    for (var p of atas.value){
      await sleep(15000);

    try{

    // console.log(c)
    //const positionMint = new PublicKey(p.account.data.parsed.info.mint)
    let positionMint = new PublicKey(p.account.data.parsed.info.mint)//positionPk.publicKey ;
    let position = await client.getPosition(
      PDAUtil.getPosition(ORCA_WHIRLPOOL_PROGRAM_ID, positionMint).publicKey,true);
    const pos_data = position.getData()
    const lala = pos_data.whirlpool
    let pool = await client.getPool(lala);
    let pool_data = pool.getData()
    let res1 = PoolUtil.getTokenAmountsFromLiquidity(
        pos_data.liquidity,
        pool_data.sqrtPrice,
        PriceMath.tickIndexToSqrtPriceX64(pos_data.tickLowerIndex),
        PriceMath.tickIndexToSqrtPriceX64(pos_data.tickUpperIndex),
        true
        )
        //console.log('first token')
        //console.log(pool.getTokenAInfo());        
        //console.log('second token')
        //console.log(pool.getTokenBInfo());
        //console.log('-------------------\n\n')        
        let token1 = DecimalUtil.fromU64(res1.tokenA,pool.getTokenAInfo().decimals).toString();
        let token2 = DecimalUtil.fromU64(res1.tokenB,pool.getTokenBInfo().decimals).toString();
        const price = PriceMath.sqrtPriceX64ToPrice(pool_data.sqrtPrice, pool.getTokenAInfo().decimals, pool.getTokenAInfo().decimals);
        const token1_address = pool.getTokenAInfo().mint;
        const token2_address = pool.getTokenBInfo().mint;

        final_res[token_map[token1_address.toBase58()]] += Number(token1) 
        final_res[token_map[token2_address.toBase58()]] += Number(token2) 
        final_res[3]+=1
        
        //if(pos_data.whirlpool.toBase58() == '7qbRF6YsyGuLUVs6Y1q64bdVrfe4ZcUUz1JRdoVNUJnm'){
        //    final_res[0]+=Number(token1);
        //    final_res[1]+=Number(token2);
        //}else if(pos_data.whirlpool.toBase58() == '8QaXeHBrShJTdtN1rWCccBxpSVvKksQ2PCu5nufb2zbk'){
        //    final_res[2]+=Number(token1);
        //    final_res[1]+=Number(token2);
        //}else{
        //    final_res[0]+=Number(token1);
        //    final_res[2]+=Number(token2);
        //}
        //console.log(token1,token2)
    }catch(e){
    //console.log('not a a whirlpool position nft account')
    //console.log(p)
}}
    console.log(final_res.toString())
};
main();
