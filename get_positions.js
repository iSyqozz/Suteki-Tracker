"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", { value: true });
const fs_1 = require("fs");
const web3_js_1 = require("@solana/web3.js");
const spl_token_1 = require("@solana/spl-token");
const whirlpools_sdk_1 = require("@orca-so/whirlpools-sdk");
const common_sdk_1 = require("@orca-so/common-sdk");
const anchor_1 = require("@project-serum/anchor");
const token_map = {
    "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v": 1,
    "So11111111111111111111111111111111111111112": 0,
    "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263": 2,
};
const main = () => __awaiter(void 0, void 0, void 0, function* () {
    const secretKeyString = (0, fs_1.readFileSync)("lp.json", { encoding: 'utf8' });
    const secretKey = Uint8Array.from(JSON.parse(secretKeyString));
    const owner = web3_js_1.Keypair.fromSecretKey(secretKey);
    //console.log(owner);
    const provider = anchor_1.AnchorProvider.env();
    const ctx = whirlpools_sdk_1.WhirlpoolContext.withProvider(provider, whirlpools_sdk_1.ORCA_WHIRLPOOL_PROGRAM_ID);
    const fetcher = new whirlpools_sdk_1.AccountFetcher(ctx.provider.connection);
    const client = (0, whirlpools_sdk_1.buildWhirlpoolClient)(ctx);
    const connection = provider.connection;
    const atas = yield connection.getParsedTokenAccountsByOwner(provider.wallet.publicKey, { programId: spl_token_1.TOKEN_PROGRAM_ID });
    const sleep = (milliseconds) => __awaiter(void 0, void 0, void 0, function* () {
        return new Promise(resolve => setTimeout(resolve, milliseconds));
    });
    let final_res = [0.0, 0.0, 0.0, 0];
    var num = 0;
    for (var p of atas.value) {
        yield sleep(15000);
        try {
            // console.log(c)
            //const positionMint = new PublicKey(p.account.data.parsed.info.mint)
            let positionMint = new web3_js_1.PublicKey(p.account.data.parsed.info.mint); //positionPk.publicKey ;
            let position = yield client.getPosition(whirlpools_sdk_1.PDAUtil.getPosition(whirlpools_sdk_1.ORCA_WHIRLPOOL_PROGRAM_ID, positionMint).publicKey, true);
            const pos_data = position.getData();
            const lala = pos_data.whirlpool;
            let pool = yield client.getPool(lala);
            let pool_data = pool.getData();
            let res1 = whirlpools_sdk_1.PoolUtil.getTokenAmountsFromLiquidity(pos_data.liquidity, pool_data.sqrtPrice, whirlpools_sdk_1.PriceMath.tickIndexToSqrtPriceX64(pos_data.tickLowerIndex), whirlpools_sdk_1.PriceMath.tickIndexToSqrtPriceX64(pos_data.tickUpperIndex), true);
            //console.log('first token')
            //console.log(pool.getTokenAInfo());        
            //console.log('second token')
            //console.log(pool.getTokenBInfo());
            //console.log('-------------------\n\n')        
            let token1 = common_sdk_1.DecimalUtil.fromU64(res1.tokenA, pool.getTokenAInfo().decimals).toString();
            let token2 = common_sdk_1.DecimalUtil.fromU64(res1.tokenB, pool.getTokenBInfo().decimals).toString();
            const price = whirlpools_sdk_1.PriceMath.sqrtPriceX64ToPrice(pool_data.sqrtPrice, pool.getTokenAInfo().decimals, pool.getTokenAInfo().decimals);
            const token1_address = pool.getTokenAInfo().mint;
            const token2_address = pool.getTokenBInfo().mint;
            final_res[token_map[token1_address.toBase58()]] += Number(token1);
            final_res[token_map[token2_address.toBase58()]] += Number(token2);
            final_res[3] += 1;
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
        }
        catch (e) {
            //console.log('not a a whirlpool position nft account')
            //console.log(p)
        }
    }
    console.log(final_res.toString());
});
main();
